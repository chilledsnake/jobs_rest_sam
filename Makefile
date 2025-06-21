.DEFAULT_GOAL := all

SRC_DIR := app
TESTS_DIR := tests

PYTHON ?= python3

# Run full validation workflow
all: imports format typecheck test

test:
	$(PYTHON) -m pytest

format:
	ruff format $(SRC_DIR) $(TESTS_DIR)

imports:
	isort $(SRC_DIR) $(TESTS_DIR)

typecheck:
	mypy $(SRC_DIR)

help:
	@echo "Available targets:"
	@echo "  all           - Run format, lint, and test"
	@echo "  format        - Format code using black"
	@echo "  help          - Show this help message"
	@echo "  test          - Run all tests"

.PHONY: all test format typecheck help
