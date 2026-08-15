from flake_triage.extract import summarize_raw_log
from flake_triage.fingerprint import normalize, pick_key_line


def test_ansi_stripped_curl_lines_cluster_together():
    a = "\x1b[31mcurl: (22) The requested URL returned error: 503\x1b[0m"
    b = "curl: (22) The requested URL returned error: 503"
    assert normalize(a) == normalize(b)


def test_bare_pid_normalized():
    a = "Sending SIGKILL to the host agent process 2904"
    b = "Sending SIGKILL to the host agent process 31337"
    assert normalize(a) == normalize(b)


def test_timestamps_and_ids_normalized():
    a = "read /sys/fs/cgroup/machine.slice/libpod-3520a47bdeadbeefcafe1234567890ab.scope/memory.stat: no such device at 03:14:21"
    b = "read /sys/fs/cgroup/machine.slice/libpod-544b1f2b00112233445566778899aabb.scope/memory.stat: no such device at 07:42:12"
    assert normalize(a) == normalize(b)


def test_go_line_numbers_normalized_but_files_kept():
    a = "/podman/test/e2e/rmi_test.go:272"
    b = "/podman/test/e2e/rmi_test.go:301"
    assert normalize(a) == normalize(b)
    assert "rmi_test.go" in normalize(a)


def test_teardown_noise_not_selected_as_key():
    summary = "\n".join(
        [
            "some setup output",
            'limactl delete --force podman-ci',
            'Deleted "podman-ci"',
            "curl: (22) The requested URL returned error: 503",
            "more output",
        ]
    )
    picked = pick_key_line(summary)
    assert picked is not None
    assert "curl: (22)" in picked[0]


def test_concrete_error_beats_test_name_line():
    summary = "\n".join(
        [
            "not ok 209 |220| podman healthcheck in 3818ms",
            "#   `assert \"$output\" =~ \"StartLimitIntervalUSec=0\"' failed",
        ]
    )
    picked = pick_key_line(summary)
    assert picked is not None
    assert "failed" in picked[0]
    assert not picked[0].startswith("not ok")


def test_no_signal_returns_none():
    assert pick_key_line("everything is fine\nnothing to see here") is None


def test_summary_step_traceback_never_selected():
    # when a job dies before producing logs, the CI summary step tracebacks on
    # its unexpanded glob; that is harness noise, not the failure
    summary = "\n".join(
        [
            "Traceback (most recent call last):",
            '  File "hack/ci/github_log_summary.py", line 120, in <module>',
            "FileNotFoundError: [Errno 2] No such file or directory: 'hack/ci/logs/*.html'",
            "curl: (22) The requested URL returned error: 503",
        ]
    )
    picked = pick_key_line(summary)
    assert picked is not None
    assert "curl: (22)" in picked[0]


def test_filenotfounderror_does_not_match_as_error_line():
    # 'FileNotFoundError:' must not be selected by the generic Error: rule
    summary = "FileNotFoundError: [Errno 2] No such file or directory: '/some/other/path'"
    picked = pick_key_line(summary)
    assert picked is None


def test_process_completed_line_never_selected():
    summary = "##[error]Process completed with exit code 2."
    assert pick_key_line(summary) is None


def test_raw_log_prefers_failure_blocks_over_expected_errors():
    # machine-test logs contain *expected* Error: lines from negative tests;
    # extraction must anchor on the real failure block instead
    log = "\n".join(
        [
            "2026-08-13T10:00:00.0000000Z some output",
            "2026-08-13T10:00:01.0000000Z Error: machine name must be 30 characters or less",
            "2026-08-13T10:00:02.0000000Z (that error was expected by a negative test)",
            "2026-08-13T10:00:03.0000000Z more output",
            "2026-08-13T10:00:04.0000000Z more output",
            "2026-08-13T10:00:05.0000000Z more output",
            "2026-08-13T10:05:00.0000000Z [FAILED] run basic podman commands",
            "2026-08-13T10:05:01.0000000Z the real failure details",
        ]
    )
    out = summarize_raw_log(log, context=2)
    assert "[FAILED]" in out
    assert "must be 30 characters" not in out


def test_raw_log_falls_back_to_error_lines_when_no_failure_block():
    log = "2026-08-13T10:00:00.0000000Z Error: something broke for real"
    out = summarize_raw_log(log)
    assert "something broke" in out


def test_generic_bats_assert_qualified_by_owning_test():
    # `is "$output" ""' failed is identical across many tests — the qualifier
    # (the owning `not ok` line) must keep unrelated tests in separate clusters
    def summary(testname):
        return "\n".join(
            [
                f"not ok 209 |220| {testname} in 3818ms",
                "# some context",
                "# `is \"$output\" \"\"' failed",
            ]
        )

    a = pick_key_line(summary("podman healthcheck"))
    b = pick_key_line(summary("podman totally different test"))
    assert a is not None and b is not None
    assert a[0] == b[0]          # same generic key line...
    assert a[2] != b[2]          # ...different qualifier => different clusters


def test_bats_sequence_number_normalized_but_file_id_kept():
    a = normalize("not ok 209 |220| podman healthcheck in 3818ms")
    b = normalize("not ok 316 |220| podman healthcheck in 12ms")
    assert a == b
    assert "|220|" in a


# --- rules ported from edsantiago/containertools (Apache-2.0) ---

def test_teardown_failure_loses_to_a_real_failure():
    # Ed's rule: a failed test often fails to clean up too; that cleanup
    # failure is expected fallout, not an independent flake
    summary = "\n".join(
        [
            "not ok 127 |065| podman cp file from container to container in 64196ms",
            "# Error: cannot remove container: in use",
            "# `basic_teardown' failed",
        ]
    )
    picked = pick_key_line(summary)
    assert picked is not None
    assert "teardown" not in picked[0]
    assert "cannot remove container" in picked[0]


def test_teardown_failure_kept_when_it_is_the_only_failure():
    # bats reports a teardown failure with its own `not ok` line, so when that
    # is all there is, the teardown IS the failure and must not be discarded
    summary = "not ok 5 teardown_suite\n# `teardown_suite' failed"
    picked = pick_key_line(summary)
    assert picked is not None
    assert "teardown_suite" in picked[0]


def test_cascade_error_outranks_everything_after_it():
    # Ed's --nuke rule: after unlinkat/EBUSY everything else is hosed
    summary = "\n".join(
        [
            "time=\"2026-08-13T10:00:00Z\" level=error msg=\"unlinkat /tmp/x: device or resource busy\"",
            "curl: (22) The requested URL returned error: 503",
            "Error: some downstream fallout",
        ]
    )
    picked = pick_key_line(summary)
    assert picked is not None
    assert "unlinkat" in picked[0]


def test_unmount_einval_is_a_cascade_error():
    summary = "Error: unmount /var/lib/containers/x: EINVAL\nError: later fallout"
    picked = pick_key_line(summary)
    assert picked is not None
    assert "unmount" in picked[0]


def test_ginkgo_seconds_spelling_normalized():
    # ginkgo prints "[4.278 seconds]"; bats prints "in 3818ms". Both are
    # volatile durations and must collapse to the same token, or identical
    # failures split into one cluster per timing value.
    a = normalize("Podman cp | • [FAILED] [4.278 seconds]")
    b = normalize("Podman cp | • [FAILED] [4.205 seconds]")
    assert a == b
    assert normalize("took 3818ms") == normalize("took 42ms")


def test_expected_error_never_becomes_the_cluster_key():
    # podman's suites provoke errors on purpose to check they are handled, and
    # bats marks them "[ rc=N (expected) ]". Clustering on one produces a key
    # that is really just the test suite working correctly. Observed live on
    # the 010-images "podman image rm --force bogus" failure.
    summary = "\n".join(
        [
            "not ok 2 |010| podman image rm --force bogus in 1087ms",
            "#   `run_podman images' failed",
            "# $ podman-remote",
            "# Error: bogus: image not known",
            "# [ rc=1 (expected) ]",
        ]
    )
    picked = pick_key_line(summary)
    assert picked is not None
    assert "bogus: image not known" not in picked[0]
    assert "run_podman images" in picked[0]


def test_unexpected_error_still_wins_over_the_test_name():
    # the counterexample: when an Error: line is NOT marked expected it is the
    # most diagnostic thing present and must still be chosen. Anchoring on the
    # `not ok` line instead would key on the test name and lose the cause.
    summary = "\n".join(
        [
            "not ok 299 [500] podman networking: port with --userns=keep-id in 4348ms",
            "#| FAIL: exit code is 126; expected 0",
            "# Error: rootlessport listen tcp 127.0.0.1:52856: bind: address already in use",
        ]
    )
    picked = pick_key_line(summary)
    assert picked is not None
    assert "address already in use" in picked[0]
