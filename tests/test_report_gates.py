from flake_triage.report import cluster_gates


def test_never_rerun_green_is_not_a_known_flake():
    # the seccomp breakage: 8 occurrences across three release branches, never
    # once green on a re-run. The maintainer called it "not a flake" by hand.
    g = cluster_gates(confirmed=0, branches="v5.8,bump_586,bump-5.8.7-dev")
    assert g["unconfirmed"]
    assert not g["catalogue_eligible"]


def test_multi_branch_breakage_still_caught():
    # the old rule required exactly one branch, so this escaped it entirely
    g = cluster_gates(confirmed=0, branches="v5.8,bump_586,bump-5.8.7-dev")
    assert g["branch_concentrated"]
    assert g["branches_seen"] == ["bump-5.8.7-dev", "bump_586", "v5.8"]


def test_single_pr_branch_is_branch_concentrated():
    g = cluster_gates(confirmed=0, branches="fix/archive-put-volume-resolution-21861")
    assert g["branch_concentrated"]
    assert not g["catalogue_eligible"]


def test_confirmed_flake_is_eligible():
    g = cluster_gates(confirmed=3, branches="main,some-pr-branch")
    assert not g["unconfirmed"]
    assert g["catalogue_eligible"]
    assert not g["branch_concentrated"]


def test_seen_on_main_is_not_branch_concentrated():
    # appearing on main means the branch is not the common factor, even with
    # no re-run confirmation yet
    g = cluster_gates(confirmed=0, branches="main")
    assert not g["branch_concentrated"]
    assert not g["catalogue_eligible"]  # still no evidence it is intermittent


def test_missing_branch_data_is_handled():
    g = cluster_gates(confirmed=0, branches=None)
    assert g["branches_seen"] == []
    assert g["branch_concentrated"]
