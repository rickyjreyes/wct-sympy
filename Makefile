PYTHON ?= python3
BUILD_DIR ?= build/reproducibility
GEOMETRY_DIR ?= ../geometry_of_resonance
CANONICAL_FILE ?= $(GEOMETRY_DIR)/WCT_FULL_EQUATION_LIST_CORRECTED.md

.PHONY: install audit registry verify reproduce clean

install:
	$(PYTHON) -m pip install --requirement reproducibility/requirements.lock

audit:
	$(PYTHON) -m pytest -q
	$(PYTHON) scripts/check_all.py
	$(PYTHON) scripts/check_full_coverage.py
	$(PYTHON) scripts/check_full_coverage.py --strict-theory
	$(PYTHON) scripts/check_lean_coverage.py

registry:
	mkdir -p $(BUILD_DIR)
	$(PYTHON) scripts/compile_registry.py \
		--canonical-file $(CANONICAL_FILE) \
		--json-out $(BUILD_DIR)/compiled-registry.json \
		--yaml-out $(BUILD_DIR)/compiled-registry.yaml \
		--report-out $(BUILD_DIR)/validation-report.json

verify:
	$(PYTHON) scripts/verify_reproducibility.py \
		--generated-registry $(BUILD_DIR)/compiled-registry.json \
		--report $(BUILD_DIR)/reproducibility-report.json

reproduce: clean audit registry verify

clean:
	rm -rf $(BUILD_DIR) reproducibility-report.json
