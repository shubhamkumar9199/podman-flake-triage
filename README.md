# podman-flake-triage

A tool that finds flaky test failures in Podman's GitHub Actions CI, works out
what each failure actually was, and writes a short report a maintainer can read
in a couple of minutes.

I built this while applying to the LFX Mentorship project "Agentic CI Flake
Categorization & Analysis" for Podman. Everything in the sample output came
from real runs against `podman-container-tools/podman`. None of it is made up
or generated from fake data.

## The problem I started from

Podman moved off Cirrus CI and onto GitHub Actions in June 2026. The old flake
tracking tooling was built around Cirrus and stopped working when Cirrus went
away. Since then no new flake issues have been filed, even though roughly a
quarter of CI runs still need a re-run to go green. So flakes are still
happening, they are just not being recorded anywhere.

There is a second problem that shaped the whole design. Podman does not retry
tests automatically. The Makefile sets `GINKGO_FLAKE_ATTEMPTS` to 0 and only
one spec in the entire tree overrides it. That means a flake here is not
"a test that failed then passed inside one run". It is a red job that a human
decided to re-run. The only place you can see it is the workflow run-attempt
layer. Most published flake detection work assumes automatic reruns, so it
does not transfer directly.

## How it works

```
discover -> attempts -> extract -> fingerprint -> classify -> report
```

Each stage is a subcommand and they all read and write one local SQLite file,
so you can stop after any stage and pick up later.

**discover** lists runs of `ci.yml` over a time window. It never uses
`?status=failure`, because that only reports the latest attempt's conclusion.
A run that failed and was then re-run to green shows up as a success and is
missing from a failure listing, which is exactly the case I care about. It also
drops `action_required` runs, since those are fork PRs waiting for approval and
never ran any tests. That is about a quarter of the raw volume.

**attempts** pulls every job across every attempt of a run in one call
(`/jobs?filter=all`) and compares conclusions per job. All attempts of a run
share the same commit SHA, so a job that failed on one attempt and passed on a
later one is a same-commit, different-outcome event. That is a confirmed flake,
and I get the label for free without annotating anything by hand.

**extract** gets the failure text. For the Linux matrix jobs it downloads the
job's log artifact and pipes the logformatter HTML through Podman's own
`hack/ci/github_log_summary.py`. I did not write my own parser. That script is
already in the repo, the maintainers wrote it, and it turns a 26 MB log into a
few KB of just the failing blocks.

Matching an artifact to the right attempt is the fiddly part. There is no API
route for per-attempt artifacts, the artifact object does not say which attempt
it came from, and a re-run uploads a second artifact with the same name. If you
just match on name you can easily grab the green re-run's log, which contains
no failure text at all. The only thing that works is checking that the
artifact's `created_at` falls inside the failing attempt's job window.

Windows and macOS machine jobs do not upload artifacts and do not run
logformatter, because the call in `win-lib.ps1` is still gated on `CIRRUS_CI`
and nothing sets that any more. Those jobs fall back to reading the raw job log.
They are also among the most frequent failures, so skipping them was not an
option.

**fingerprint** normalizes one error line per failure and uses it as a cluster
key. Timestamps, container IDs, PIDs, durations and line numbers get replaced
with placeholders so the same failure lands in the same cluster. A few of these
rules came from watching real logs go wrong: ANSI colour codes split identical
curl failures into two clusters until I stripped them, and one lima failure
fragmented into six clusters because nothing was normalizing bare process IDs.

The key stays deliberately narrow and the wider context window is kept
separate. Widening the key hurts dedup a lot, and the wide window only needs to
be looked at once per cluster.

**classify** works in two tiers. First a small set of regex rules for the
infrastructure failures that keep coming back, like curl 5xx responses when
fetching a VM image, or the lima host agent getting killed. These are certain,
free, and need no model. Anything the rules do not recognise goes to a language
model, once per cluster, never once per occurrence.

The model has to quote its evidence, and the quote is checked against the log
before the answer is accepted. If the quoted text is not really in the log
window, the whole answer is thrown away and recorded as rejected. I care about
this because the failure mode that gets LLM analysis dismissed upstream is
confident claims the log does not support. A verdict nobody can trace back to a
line is not worth reading.

**report** writes two files. A digest for a human to read, and a draft
`known-flakes.yaml` shaped like the catalog proposed in Podman issue #28870, so
the output could feed the flake-detection idea the maintainers already
sketched.

Opening issues and posting PR comments is where this should end up, and it is
not wired up yet on purpose. The analysis has to be trustworthy first, and a
person should read the output for a while before anything writes to the tracker
by itself. When it does get wired up it should be opt-in, with a maintainer able
to dismiss what is wrong, rather than on by default for everyone.

## What I measured

From a 10 day window against the real repo:

| | |
|---|---|
| runs analyzed | 174 |
| failing job records | 305 |
| confirmed flakes (fail then pass at the same commit) | 62 |
| failure signatures grouped into clusters | 225 into 61 (73% dedup) |
| occurrences classified with no model involved | 29% |
| confirmed flakes wrongly called a real regression | 0 |

Full numbers, including where the pipeline loses coverage, are in
[docs/sample-output/evaluation.md](docs/sample-output/evaluation.md).

Two results are worth calling out because they are the point of the design.

The single most common failure signature in that window was not a flake at all.
One test failed 37 times across 13 different matrix jobs, all on one pull
request's branch, and never once passed on a re-run. That is a PR breaking a
test, not a flaky test. The tool flags it and keeps it out of the flake catalog
based on where and how it failed, not on what the log text looks like.

The evidence check earns its place. When I first ran the model tier, a lot of
its quoted evidence did not survive verification. Tightening it too far was
also wrong: for a while the check demanded a single line, and it started
rejecting honest quotes, because Ginkgo assertion output is several lines by
nature. It now accepts a contiguous block of lines and still rejects text
stitched together from lines that were not next to each other. Each version of
that check is recorded with the numbers it produced.

## Running it

```console
pip install -e '.[dev]'
gh auth login                  # or export GITHUB_TOKEN

flake-triage sync --days 10    # discover runs, diff attempts
flake-triage extract           # pull failure evidence
flake-triage fingerprint       # normalize and cluster
flake-triage classify          # regex tier only
flake-triage report            # digest.md and known-flakes.yaml
flake-triage evaluate          # measure against the confirmed flakes
```

To use the model tier as well, pick a provider:

```console
flake-triage classify --llm ollama      # local model
flake-triage classify --llm anthropic
flake-triage classify --llm openai
```

Rules and prompts change often while you are tuning, so
`fingerprint --rebuild`, `classify --rebuild` and `extract --retry-empty`
recompute derived data instead of leaving stale rows behind.

Settings come from the environment: `FT_REPO`, `FT_WORKFLOW`, `FT_DATA_DIR`,
`GITHUB_TOKEN`, and whichever model provider keys you use.

## Work this builds on

- `timcoding1988/container-flake-mgmt`, which grouped failures by CI matrix so
  a platform-specific failure is not mistaken for flakiness. I kept that idea.
  Its ingestion was written for Cirrus, so it cannot run today.
- `edsantiago/containertools`, the old flake catalog. Its README says plainly
  that nobody should expect to reuse it. The manual step in it, where a person
  reads an error and remembers which issue it belongs to, is the step this tool
  is trying to take over.
- Kubernetes `test-infra/triage`, for the normalization and clustering approach.
- An et al., "Just-in-Time Flaky Test Detection via Abstracted Failure Symptom
  Matching" (arXiv 2310.06298), which matches failure symptoms without needing
  reruns. That fits Podman, where there are no reruns to lean on.
- Podman issue #28870, which sketches a `known-flakes.yaml` catalog and a
  `/retrigger` command. The report output is shaped to fit it.

## What this does not do yet

- Clusters are exact-key only. Two failures that are clearly the same problem
  but differ slightly in wording stay separate. Near-duplicate merging is the
  obvious next step.
- Category accuracy is not measured. Confirmed flakes tell me a failure was
  flaky, not which category it belongs to, so per-category accuracy needs a
  sample checked by hand. I did not want to claim a number I had not measured.
- Discovery works on a time window, so a run that gets re-run long after it
  ages out of that window is missed.
- CI logs are treated as untrusted input and the model is told to treat log
  content as data. That reduces the risk of a log talking the model into
  something, it does not eliminate it.
