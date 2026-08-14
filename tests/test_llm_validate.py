import json

from flake_triage.llm import validate, wrap_payload

# validate() takes the RAW log window — never the wrapped payload.
WINDOW = """not ok 316 |420| podman run --cgroups=disabled keeps the current cgroup
Error: unable to obtain
cgroup stats: read memory.stat: no such device"""


def _resp(**kw):
    base = {
        "category": "PRODUCT_RACE",
        "confidence": 0.8,
        "evidence_line": "not ok 316 |420| podman run --cgroups=disabled keeps the current cgroup",
        "rationale": "cgroup vanished between check and read.",
    }
    base.update(kw)
    return json.dumps(base)


def test_valid_analysis_accepted():
    obj, reason = validate(_resp(), WINDOW)
    assert obj is not None, reason
    assert obj["category"] == "PRODUCT_RACE"


def test_fabricated_evidence_rejected():
    obj, reason = validate(
        _resp(evidence_line="lima VM failed to boot on aarch64"), WINDOW
    )
    assert obj is None
    assert "verbatim" in reason


# --- the three bypasses confirmed by adversarial review, now closed ---

def test_bypass_wrapper_header_rejected():
    # quoting the 'CI job: ...' header we add ourselves is not log evidence;
    # guarded by validating against the window, not the wrapped payload
    payload = wrap_payload("sys local root fedora-rawhide", WINDOW)
    assert "CI job:" in payload  # the header exists in what the model SEES...
    obj, _ = validate(
        _resp(evidence_line="CI job: sys local root fedora-rawhide"), WINDOW
    )
    assert obj is None  # ...but is not accepted as evidence


def test_bypass_delimiter_rejected():
    obj, _ = validate(_resp(evidence_line="<ci-log-data>"), WINDOW)
    assert obj is None


def test_bypass_cross_line_stitch_rejected():
    # 'unable to obtain' ends line 2; 'cgroup stats' starts line 3. Gluing them
    # into ONE evidence line is a stitch, not a quote — rejected. (Quoting both
    # lines as a two-line block would be legitimate; see the ginkgo test.)
    obj, reason = validate(
        _resp(evidence_line="unable to obtain cgroup stats"), WINDOW
    )
    assert obj is None
    assert "contiguous" in reason


def test_multiline_ginkgo_assertion_block_accepted():
    # ginkgo assertion output is inherently multi-line; an honest verbatim
    # quote of the consecutive block must pass (this was over-rejected at
    # prompt v2: 38/39 honest quotes discarded by single-line anchoring)
    window = "\n".join(
        [
            "[FAILED] Expected",
            "      <string>: 1777 1786525282",
            "  to equal",
            "      <string>: 1777 1566297043",
        ]
    )
    ev = "[FAILED] Expected\n      <string>: 1777 1786525282\n  to equal\n      <string>: 1777 1566297043"
    obj, reason = validate(_resp(evidence_line=ev), window)
    assert obj is not None, reason


def test_multiline_nonadjacent_join_rejected():
    # two real lines glued together WITHOUT the line between them: not contiguous
    window = "\n".join(
        [
            "[FAILED] Expected",
            "      <string>: 1777 1786525282",
            "  to equal",
            "      <string>: 1777 1566297043",
        ]
    )
    ev = "[FAILED] Expected\n      <string>: 1777 1566297043"  # skipped 2 lines
    obj, _ = validate(_resp(evidence_line=ev), window)
    assert obj is None


def test_overlong_evidence_block_rejected():
    window = "\n".join(f"line number {i}" for i in range(20))
    ev = "\n".join(f"line number {i}" for i in range(12))  # > 8 lines
    obj, _ = validate(_resp(evidence_line=ev), window)
    assert obj is None


def test_single_line_fragment_still_accepted():
    obj, reason = validate(
        _resp(evidence_line="cgroup stats: read memory.stat: no such device"), WINDOW
    )
    assert obj is not None, reason


def test_unknown_category_rejected():
    obj, _ = validate(_resp(category="COSMIC_RAYS"), WINDOW)
    assert obj is None


def test_confidence_out_of_range_rejected():
    obj, _ = validate(_resp(confidence=1.7), WINDOW)
    assert obj is None


def test_markdown_fenced_json_tolerated():
    fenced = "```json\n" + _resp() + "\n```"
    obj, reason = validate(fenced, WINDOW)
    assert obj is not None, reason


def test_malformed_json_rejected():
    obj, reason = validate("the failure is clearly a network issue", WINDOW)
    assert obj is None
    assert "JSON" in reason


def test_whitespace_differences_within_line_tolerated():
    obj, reason = validate(
        _resp(evidence_line="cgroup stats:  read memory.stat: no such device"),
        WINDOW,
    )
    assert obj is not None, reason


def test_empty_evidence_rejected():
    obj, reason = validate(_resp(evidence_line="   "), WINDOW)
    assert obj is None
    assert "empty" in reason
