.DEFAULT_GOAL := all

SRC_DIR := app
TESTS_DIR := tests

PYTHON ?= python3

# Run full validation workflow
all: format typecheck test

format:
	ruff format $(SRC_DIR) $(TESTS_DIR) && ruff check --fix $(SRC_DIR) $(TESTS_DIR)

typecheck:
	mypy $(SRC_DIR)

test:
	$(PYTHON) -m pytest

help:
	@echo "Available targets:"
	@echo "  all           - Run format, lint, and test"
	@echo "  format        - Format code using black"
	@echo "  typecheck     - Run type checking with mypy"
	@echo "  test          - Run all tests"
	@echo "  help          - Show this help message"

.PHONY: all format typecheck test help
