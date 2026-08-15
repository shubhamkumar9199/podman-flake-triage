from flake_triage.merge import (
    bounded_edit_distance,
    ngram_profile,
    profile_lower_bound,
    should_merge,
)


def test_identical_signatures_merge():
    s = "curl: (22) The requested URL returned error: 503"
    assert should_merge(s, s)


def test_near_duplicates_merge():
    # same failure, one differing path component
    a = "Error: unable to start container abc: cannot open /run/user/1000/ctr/state"
    b = "Error: unable to start container abc: cannot open /run/user/1001/ctr/state"
    assert should_merge(a, b)


def test_genuinely_different_failures_do_not_merge():
    a = "curl: (22) The requested URL returned error: 503"
    b = "Error: unable to obtain cgroup stats: no such device"
    assert not should_merge(a, b)


def test_short_signatures_require_exact_match():
    # at this length a few characters is a real difference, so no fuzz
    assert not should_merge("Error: EBUSY", "Error: EAGAIN")


def test_similar_but_distinct_curl_codes_stay_apart():
    # (22) and (56) are different failure modes and must not be merged
    a = "curl: (22) The requested URL returned error: 503 Service Unavailable"
    b = "curl: (56) Connection died, tried 5 times before giving up entirely"
    assert not should_merge(a, b)


def test_lower_bound_never_exceeds_true_distance():
    # the prefilter must never reject a pair it should have kept
    pairs = [
        ("podman run --rm alpine echo hello world today", "podman run --rm alpine echo hello world"),
        ("the quick brown fox jumps over the lazy dog", "the quick brown fox leaps over the lazy dog"),
    ]
    for a, b in pairs:
        lb = profile_lower_bound(ngram_profile(a), ngram_profile(b))
        true = bounded_edit_distance(a, b, 10_000)
        assert lb <= true, f"lower bound {lb} exceeded true distance {true}"


def test_bounded_distance_gives_up_at_limit():
    a = "a" * 100
    b = "b" * 100
    assert bounded_edit_distance(a, b, 5) == 5


def test_bounded_distance_exact_when_under_limit():
    assert bounded_edit_distance("kitten", "sitting", 100) == 3
