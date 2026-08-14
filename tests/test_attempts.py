from flake_triage.attempts import diff_attempts, job_key


def _j(attempt, conclusion, jid):
    return {"run_attempt": attempt, "conclusion": conclusion, "id": jid}


def test_fail_then_pass_is_a_transition():
    transitions, persistent = diff_attempts([_j(1, "failure", 10), _j(2, "success", 20)])
    assert transitions == [(1, 2, 10)]
    assert persistent == 0


def test_fail_then_fail_is_persistent():
    transitions, persistent = diff_attempts([_j(1, "failure", 10), _j(2, "failure", 20)])
    # attempt-1 failure was re-run and failed again -> persistent;
    # attempt-2 failure is the final attempt -> neither (never re-run)
    assert transitions == []
    assert persistent == 1


def test_fail_on_final_attempt_is_not_persistent():
    transitions, persistent = diff_attempts([_j(1, "failure", 10)])
    assert transitions == []
    assert persistent == 0


def test_job_absent_from_later_attempt_keeps_conclusion():
    # green job at attempt 1 is not re-run at attempt 2 (rerun-failed-only):
    # its absence is not a failure and not a transition
    transitions, persistent = diff_attempts([_j(1, "success", 10)])
    assert transitions == []
    assert persistent == 0


def test_multiple_fails_then_pass_yields_one_transition_per_fail():
    transitions, _ = diff_attempts(
        [_j(1, "failure", 10), _j(2, "failure", 20), _j(3, "success", 30)]
    )
    assert (1, 3, 10) in transitions
    assert (2, 3, 20) in transitions


def test_unordered_input_is_sorted():
    transitions, _ = diff_attempts([_j(2, "success", 20), _j(1, "failure", 10)])
    assert transitions == [(1, 2, 10)]


def test_cancelled_and_skipped_are_not_failures():
    transitions, persistent = diff_attempts(
        [_j(1, "cancelled", 10), _j(2, "success", 20)]
    )
    assert transitions == []
    assert persistent == 0


def test_job_key_strips_lima_suffix_and_keeps_double_spaces():
    assert job_key("int local root fedora-rawhide / lima") == "int local root fedora-rawhide"
    # empty matrix fields produce double spaces — preserved, it is the identity
    assert job_key("bindings  root fedora-current / lima") == "bindings  root fedora-current"
    assert job_key("windows machine hyperv") == "windows machine hyperv"
