.PHONY: build-FastAPILayer

build-FastAPILayer:
    # $(ARTIFACTS_DIR) is provided by AWS SAM, pointing to
    # the folder where final build assets should be placed.

    mkdir -p "$(ARTIFACTS_DIR)/python"

    # Copy any .py files that should live in the layer (if needed)
    # cp some_file.py "$(ARTIFACTS_DIR)/python"

    # Install dependencies into the python/ folder inside artifacts
    python -m pip install --no-cache-dir -r requirements.txt -t "$(ARTIFACTS_DIR)/python"