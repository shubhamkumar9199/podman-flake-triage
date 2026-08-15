# Design notes

Why this tool is built the way it is. Each decision below says what it does,
why, and what was rejected.

## Polling instead of a GitHub App

The tool asks the GitHub API for data on a schedule. It does not receive
webhooks.

This is not a shortcut. Webhooks and GitHub Apps need admin rights on the
repository being watched, and an outside contributor does not have those. So
polling is the only thing actually available. It also turns out to be enough.
Conditional requests mean asking about the same window twice costs almost
nothing against the hourly limit, and the artifact download redirects to blob
storage, which does not count at all. A full ten day sync used well under a
fifth of the hourly budget.

If the project ever adopts this, a maintainer could install it as an App and
get events pushed instead. Nothing in the design would have to change, because
the stages read from the database rather than from whatever delivered the data.

## Comparing attempts is what finds flakes

Podman does not retry tests automatically. `GINKGO_FLAKE_ATTEMPTS` is `0` in
the Makefile, and exactly one spec in the whole tree overrides it.

This single fact decides the design. A flake here is not a test that failed and
passed inside one run. It is a red job that a person decided to re-run. The
only place that is visible is the workflow attempt layer.

It also means most of the published work on flake detection does not transfer.
DeFlaker, Chromium's FindIt and Meta's flakiness score all learn from automatic
reruns. There are none here to learn from. The approach that does fit is
matching failure symptoms without reruns, which is what An et al. describe in
arXiv 2310.06298.

The upside is large. Every attempt of a run shares one commit SHA, so a job
that failed on one attempt and passed on a later one failed and passed on
identical code. That is a flake, proven, and it costs nothing to label. The
evaluation corpus is built entirely from these, with no manual annotation.

What was rejected: asking the API for failed runs only. That reports the
latest attempt's conclusion, so a run that failed and was re-run to green comes
back as a success and never appears. Those are exactly the flakes.

## One SQLite file, no services

State lives in a single SQLite file in WAL mode.

Volume does not justify anything bigger. Podman produces roughly two hundred
failing jobs a week, so months of history fits comfortably in one file, and
there is only ever one writer. More importantly, a tool that a single person
has to keep running should not need infrastructure behind it to stay alive.

The prior art supports this. Ed Santiago's flake catalogue ran on SQLite for
years and reached 4.1 GB. What killed it was not the database, it was that only
one person could run it and the output went to a personal host rather than
anywhere the project owned.

A real database, a queue and object storage would make sense once the tool is
project-owned and more than one thing reads from it. That belongs in a later
phase, not in a prototype.

## Reusing Podman's own log extraction

Artifact HTML goes through `hack/ci/github_log_summary.py` from the Podman
repository, vendored unmodified with a note saying where it came from.

Writing a parser instead would be slower, worse, and pointless. That script is
already in the tree, the CI already uses it to build the failure summary on the
run page, and it reduces a 26 MB job log to a few KB containing only the
failing blocks. It was merged on 7 August 2026, days before this was built.

Windows and macOS machine jobs are a different story. They upload no artifacts
and never run logformatter, because the call in `hack/ci/win-lib.ps1` is still
gated behind `CIRRUS_CI`, and nothing has set that variable since Cirrus was
removed in June. Those jobs fall back to reading the raw job log. They are also
among the most failure-prone in the matrix, so the least instrumented platform
is the one failing most. That is worth fixing upstream and it is a one line
change.

## Matching artifacts to attempts by time

An artifact is attributed to a specific attempt by checking it was created
inside that attempt's job window.

Nothing else works. There is no API route for per-attempt artifacts. The
artifact object carries no attempt number. And a re-run uploads a second
artifact with an identical name, so matching on name can hand you the green
re-run's log instead of the failing one.

The reason this matters more than it sounds: getting it wrong does not throw an
error. You get a log with no failures in it, which looks exactly like a job
that was fine.

## A narrow grouping key, a wide window for the model

Failures are grouped by one normalised error line. The wider context around
that line is stored separately and only looked at once per group.

Widening the key destroys grouping. Measured on real failures, a three to five
line key kept about three quarters of the duplication collapsed, while a forty
line key kept under half. Since the wide context is what a model reads, keeping
the two separate means grouping stays tight while the model still gets enough
to work with.

Three normalisation rules came from watching real logs fall apart:

Colour codes have to be stripped first. Identical curl failures were landing in
two different groups purely because some carried escape sequences.

Bare process ids need their own rule. The Kubernetes rule set this borrows from
has none, so one lima failure fragmented into six groups that were all the same
thing.

Bats sequence numbers shift between runs while the file id stays stable, so
keying on the sequence number splits one recurring failure into many.

Three kinds of noise are excluded from ever being chosen as a key: the lima
teardown the CI traps on exit, the exit code line GitHub appends to every
failed job, and the traceback the summary script itself produces when a job
died before writing any logs. All three sit next to real failures, and all
three are meaningless as a grouping key.

## Rules before the model

Every group is checked against a small set of rules first. Only what the rules
do not recognise goes to a model, and then once per group rather than once per
failure.

The rules cover the failures that keep recurring: curl giving up on an external
fetch, the lima host agent having to be killed, a runner out of disk, a suite
hitting its deadline. These are certain and free. In the measured window they
handled 29% of all occurrences with no model involved at all.

Cost is not the main argument, since either way this is a few dollars a year.
The argument is trust. The rules keep working if a model is unavailable, or
changed, or simply wrong, and a maintainer can read a rule and agree with it.

One rule is worth calling out. A suite timeout is classified as a timeout, not
as a problem with whichever test was named, because ginkgo prints whatever
happened to be running when the clock ran out. Blaming that test is wrong in a
way that wastes somebody's afternoon.

## The evidence check

Any verdict from a model must quote the log line it rests on, and that quote is
checked against the log before the verdict is kept. If the quoted text is not
really there, the whole answer is discarded and recorded as rejected along with
the reason. Answering "unknown" with low confidence is allowed and stored.

This is the most important thing in the tool. The way this kind of analysis
loses trust is confident claims the log does not support, and instructing a
model to be careful does not prevent that. Making an unsupported verdict
impossible to publish does.

Getting the check right took three versions, and the middle one was wrong in an
instructive way.

| version | rule | result on 96 groups |
|---|---|---|
| 1 | quote appears anywhere in the prompt | 91 accepted, but the check was foolable, so acceptance meant little |
| 2 | quote must sit inside one log line | 39 rejected, and a retry re-rejected 38 of those 39 |
| 3 | quote must be a contiguous block of lines | 37 of those 38 accepted, 1 genuine rejection |

Version 1 was too loose in three separate ways, all found by deliberately
attacking it. The quote could be the wrapper text the tool adds itself, or the
markers around the log data, or two lines glued together that were never next
to each other, because whitespace was being flattened across the whole prompt
before comparing.

Version 2 fixed all three and then rejected honest answers, which only became
clear from reading an actual rejection. Ginkgo prints an assertion across
several lines, so quoting it correctly means quoting all of them, and demanding
a single line punished the model for doing the right thing.

Version 3 accepts a contiguous run of lines and still refuses text stitched
from lines that were not adjacent. Each version is recorded with the numbers it
produced, so the change is auditable rather than asserted.

Separately, log content is wrapped in explicit data markers and the model is
told it is untrusted input. A CI log contains whatever a test decided to print,
which means anyone who can run CI can put text in there aimed at whatever reads
it later.

## Inheriting from the retired flake catalogue

`edsantiago/containertools` is still online and Apache-2.0 licensed. The tools
in it are dead in exactly one place: they fetched logs from
`api.cirrus-ci.com`, which no longer exists. Almost nothing else in them was
Cirrus-specific. The error normalisation, the test-name canonicalisation and
the rules about which log lines are noise are Podman knowledge, and Podman
still exists.

Two rules were worth porting, both encoding triage experience that nobody
would derive from first principles.

**Teardown failures are secondary.** From `cirrus-flake-summarize`: do not
count a teardown failure as a flake when there are other failures, because it
just means a failed test did not clean up after itself. That is expected
fallout. On the sample corpus this rule fixed a real case: a `065-cp` failure
was keying on `basic_teardown` rather than on the failure that caused it.

**Cascade errors poison everything after them.** `cirrus-flake-assign` had a
`--nuke` flag to delete all other flakes in a task, used for the
`unlinkat`/EBUSY and `unmount`/EINVAL cases where everything downstream is
garbage. There it was a human decision made afterwards; here the cascade error
simply outranks anything following it in the same job.

Two other rules were arrived at here independently before that code was found:
stripping the leading logformatter offset, and dropping bats timing suffixes.
`cirrus-flake-summarize` does both. Two people hitting the same rocks years
apart is reasonable evidence the approach is right.

The part of that toolchain worth noticing most is what it did *not* automate.
`cirrus-flake-assign` is a human typing "these failures belong to issue
#12345". Everything around that step was scripted; the judgement itself never
was, and it stopped happening when its author left. That is the gap this tool
is aimed at.

## Metadata beats reading the text

Some conclusions cannot be reached by reading a log at all.

If every occurrence of a failure sits on one branch that is not `main`, and not
one of them ever passed on a re-run, that is almost certainly that pull request
breaking a test rather than a flake.

This is not hypothetical. In the measured window the single most common failure
signature was one test failing 37 times across 13 matrix jobs, all on one
branch, never green on a re-run. The model read the log and called it a test
bug, which is a fair reading of the text, and it was still the wrong answer.
What caught it was information the log does not contain.

Those are marked in the digest and excluded from the flake catalogue whatever
the text says, because a catalogue of known flakes containing somebody's broken
branch is worse than no catalogue.

## Output is files, for now

The tool writes a digest and a draft catalogue. It does not open issues or post
comments.

The project brief does ask for that eventually, and it should happen. The
sensible order is to make the analysis trustworthy first and let a person read
the output for a while before anything writes to the tracker on its own. When it
does, it should be opt-in with a maintainer able to dismiss what is wrong,
which is also the position the lead maintainer took on podman#28141 about
review bots: if contributors are expected not to submit unverified output, the
project should not send them any either.

The catalogue is shaped like the one sketched in podman#28870, so the output
fits an integration point the maintainers already described.

## Honest measurement or none

The evaluation reports coverage stage by stage, so it is visible how many
confirmed flakes survived extraction, then grouping, then classification, and
where the rest were lost.

It does not report classification accuracy. A re-run going green proves a
failure was flaky. It says nothing about whether the cause was a network
problem or a race, so there is nothing to check a category against. Measuring
that needs a sample gone through by hand, and publishing a number without one
would mean inventing it.

There is one check ground truth can do properly, and it runs in the opposite
direction: a failure confirmed flaky should never be classified as a real
regression. That count is reported and it is zero.

## What a review found

The evidence check and the extraction paths were deliberately attacked to see
what would break. Twelve problems were confirmed and fixed, and the test count
went from 21 to 43.

Besides the three ways the evidence check could be fooled, the confirmed
problems were: an expired artifact would crash the whole stage rather than
costing one job, a partly downloaded file would be trusted forever afterwards
because the code only checked whether the file existed, an artifact that
matched but contained no failure text never fell back to the raw log, downloads
had no retry while everything else did, and the model call budget counted
successes rather than attempts, so a failing provider could be retried
indefinitely without the budget moving.

One limitation was documented rather than fixed. Discovery works on a time
window, so a run re-run long after it ages out of that window is never
re-examined. Polling individual runs by their update time would fix it and is
cheap with conditional requests. It did not make the cut for a prototype.
