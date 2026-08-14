from flake_triage.extract import match_artifact


def _job(key="sys local root fedora-rawhide",
         start="2026-08-12T10:00:00Z", end="2026-08-12T11:00:00Z"):
    return {"job_key": key, "started_at": start, "completed_at": end}


def _art(name="sys-local-root-fedora-rawhide.logs",
         created="2026-08-12T11:05:00Z", expired=False, aid=1):
    return {"name": name, "created_at": created, "expired": expired, "id": aid,
            "archive_download_url": "https://example.invalid"}


def test_artifact_in_window_matches():
    assert match_artifact(_job(), [_art()])["id"] == 1


def test_expired_artifact_skipped():
    # the listing still returns expired artifacts; downloading them is a 410
    assert match_artifact(_job(), [_art(expired=True)]) is None


def test_wrong_attempt_artifact_rejected_by_time_window():
    # same name, uploaded hours later by the green re-run: must not match
    late = _art(created="2026-08-12T14:25:00Z", aid=2)
    assert match_artifact(_job(), [late]) is None


def test_name_collision_across_attempts_resolved_by_window():
    # two artifacts with identical names (one per attempt) — only the one
    # inside the failing attempt's window may match
    a1 = _art(created="2026-08-12T11:05:00Z", aid=1)
    a2 = _art(created="2026-08-12T14:25:00Z", aid=2)
    assert match_artifact(_job(), [a2, a1])["id"] == 1


def test_wrong_name_rejected():
    other = _art(name="int-local-root-fedora-rawhide.logs")
    assert match_artifact(_job(), [other]) is None


def test_artifact_before_job_start_rejected():
    early = _art(created="2026-08-12T09:00:00Z")
    assert match_artifact(_job(), [early]) is None
