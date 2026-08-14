"""Thin GitHub REST client: pagination, retries, rate-limit awareness, ETag cache.

Intentionally not a GitHub App: this tool runs *outside* the target repo
(no webhook or app-install rights on podman-container-tools/podman), so
authenticated polling with conditional requests is the only viable — and a
fully sufficient — integration. A job-log/artifact fetch costs ~1 rate-limit
unit (the 302); the Azure blob download itself is free.
"""

from __future__ import annotations

import contextlib
import json
import logging
import os
import sqlite3
import time
from collections.abc import Iterator
from datetime import UTC, datetime
from typing import Any

import requests

log = logging.getLogger(__name__)

API = "https://api.github.com"
RETRYABLE = {500, 502, 503, 504}


class GitHub:
    def __init__(self, token: str, conn: sqlite3.Connection | None = None):
        self.s = requests.Session()
        self.s.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "podman-flake-triage",
            }
        )
        self.conn = conn  # for the http_cache table; optional

    # -- core ---------------------------------------------------------------

    def get(self, path: str, params: dict[str, Any] | None = None, *, cache: bool = False) -> Any:
        """GET one page of JSON, with retries and optional ETag conditional caching."""
        url = path if path.startswith("http") else f"{API}{path}"
        # requests encodes params into the URL; build the cache key the same way
        req = requests.Request("GET", url, params=params).prepare()
        cache_key = req.url or url

        headers = {}
        cached = self._cache_get(cache_key) if cache else None
        if cached is not None and cached["etag"]:
            headers["If-None-Match"] = cached["etag"]

        for attempt in range(4):
            resp = self.s.get(url, params=params, headers=headers, timeout=60)
            if resp.status_code == 304 and cached is not None:
                return json.loads(cached["body"])
            if resp.status_code in RETRYABLE:
                wait = 2**attempt
                log.warning("GET %s -> %s, retrying in %ss", cache_key, resp.status_code, wait)
                time.sleep(wait)
                continue
            if resp.status_code == 403 and resp.headers.get("X-RateLimit-Remaining") == "0":
                reset = int(resp.headers.get("X-RateLimit-Reset", "0"))
                wait = max(0, reset - int(time.time())) + 2
                if wait > 600:
                    raise RuntimeError(f"Rate limit exhausted; resets in {wait}s. Stopping.")
                log.warning("Primary rate limit hit; sleeping %ss", wait)
                time.sleep(wait)
                continue
            if resp.status_code == 429 or (
                resp.status_code == 403 and "Retry-After" in resp.headers
            ):
                wait = int(resp.headers.get("Retry-After", "30"))
                log.warning("Secondary rate limit; sleeping %ss", wait)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            remaining = resp.headers.get("X-RateLimit-Remaining")
            if remaining and int(remaining) % 500 == 0:
                log.info("Rate limit remaining: %s", remaining)
            if cache and resp.headers.get("ETag"):
                self._cache_put(cache_key, resp.headers["ETag"], resp.content)
            return resp.json()
        raise RuntimeError(f"GET {cache_key}: retries exhausted")

    def paginate(
        self, path: str, params: dict[str, Any] | None = None, *, item_key: str | None = None
    ) -> Iterator[dict[str, Any]]:
        """Yield items across all pages (Link-header driven)."""
        params = dict(params or {})
        params.setdefault("per_page", 100)
        page = 1
        while True:
            params["page"] = page
            data = self.get(path, params, cache=True)
            items = data[item_key] if item_key else data
            if not items:
                return
            yield from items
            # trust the count instead of parsing Link: full page => maybe more
            if len(items) < params["per_page"]:
                return
            page += 1

    def download(self, url: str, dest_path: str) -> int:
        """Stream a (possibly redirected) download to disk. Returns bytes written.

        Atomic: streams to a .part file and renames on success, so an
        interrupted download can never leave a truncated file that a
        `path.exists()` cache check would then trust forever. Retries
        transient failures like get() does.
        """
        part = dest_path + ".part"
        last_err: Exception | None = None
        for attempt in range(3):
            try:
                with self.s.get(url, timeout=300, stream=True, allow_redirects=True) as resp:
                    if resp.status_code in RETRYABLE:
                        raise requests.HTTPError(f"HTTP {resp.status_code}", response=resp)
                    resp.raise_for_status()
                    n = 0
                    with open(part, "wb") as f:
                        for chunk in resp.iter_content(1 << 16):
                            f.write(chunk)
                            n += len(chunk)
                os.replace(part, dest_path)
                return n
            except requests.RequestException as e:
                last_err = e
                status = getattr(getattr(e, "response", None), "status_code", None)
                if status is not None and status not in RETRYABLE and status != 429:
                    break  # 404/410/403: retrying will not help
                wait = 2**attempt
                log.warning("download %s failed (%s), retrying in %ss", url, e, wait)
                time.sleep(wait)
        with contextlib.suppress(OSError):
            os.remove(part)
        raise RuntimeError(f"download failed: {url}: {last_err}")

    # -- etag cache ----------------------------------------------------------

    def _cache_get(self, url: str) -> sqlite3.Row | None:
        if self.conn is None:
            return None
        return self.conn.execute(
            "SELECT etag, body FROM http_cache WHERE url = ?", (url,)
        ).fetchone()

    def _cache_put(self, url: str, etag: str, body: bytes) -> None:
        if self.conn is None:
            return
        self.conn.execute(
            "INSERT INTO http_cache(url, etag, body, fetched_at) VALUES(?,?,?,?) "
            "ON CONFLICT(url) DO UPDATE SET etag=excluded.etag, body=excluded.body, "
            "fetched_at=excluded.fetched_at",
            (url, etag, body, datetime.now(UTC).isoformat()),
        )
        self.conn.commit()
