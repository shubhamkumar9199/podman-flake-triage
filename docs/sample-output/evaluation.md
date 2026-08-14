# Evaluation — 2026-08-13 23:30 UTC

## Corpus (all measured live from GHA, no synthetic data)
- runs analyzed: 174 (64 with >1 attempt, 37%)
- failing job records: 305
- ground truth: 62 confirmed flakes (FAIL→PASS, same head_sha)

## Pipeline coverage over the confirmed-flake corpus
- evidence extracted: 48/62 (77%)
- fingerprinted:      48/62 (77%)
- classified:         48/62 (77%)

## Dedup / cost
- failure signatures: 225  → clusters: 106 (dedup 53%)
- no extractable signal: 0
- occurrences classified by regex tier (no LLM): 65 (29% of classified)
- occurrences needing LLM tier: 160

## Sanity checks
- confirmed flakes classified GENUINE_REGRESSION: 0

## Category distribution (clusters weighted by occurrences)
- TEST_BUG [llm]: 93
- NETWORK_INFRA [regex]: 45
- VM_INFRA [llm]: 24
- TEST_TIMEOUT [llm]: 17
- HARNESS [regex]: 12
- NETWORK_INFRA [llm]: 12
- PRODUCT_RACE [llm]: 6
- TEST_TIMEOUT [regex]: 5
- UNKNOWN [llm]: 3
- HARNESS [llm]: 2
- PARALLEL_INTERFERENCE [llm]: 2
- RUNNER_INFRA [regex]: 2
- PRODUCT_RACE [regex]: 1
- RUNNER_INFRA [llm]: 1

## Known limitations (stated, not hidden)
- FAIL→PASS labels *flakiness*, not category; per-category accuracy needs
  a human-audited sample and is not claimed here.
- Jobs with expired/absent logs and artifacts produce no evidence and are
  counted as pipeline losses above, not silently dropped.
- A re-run that stays red is treated as persistent, but a flake can in
  principle fail twice; multi-attempt persistence is evidence, not proof.
