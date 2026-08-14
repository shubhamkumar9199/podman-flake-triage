PY := .venv/bin/python

.PHONY: setup test lint fmt pipeline eval clean

setup:
	python3 -m venv .venv
	.venv/bin/pip install -e '.[dev]'

test:
	$(PY) -m pytest tests/ -q

lint:
	$(PY) -m ruff check flake_triage/ tests/

fmt:
	$(PY) -m ruff format flake_triage/ tests/

# full pipeline against live data (regex tier only; add LLM=anthropic|ollama)
pipeline:
	$(PY) -m flake_triage sync --days 10
	$(PY) -m flake_triage extract
	$(PY) -m flake_triage fingerprint
	$(PY) -m flake_triage classify $(if $(LLM),--llm $(LLM))
	$(PY) -m flake_triage report

eval:
	$(PY) -m flake_triage evaluate

clean:
	rm -rf data/artifacts
