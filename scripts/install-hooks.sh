#!/usr/bin/env bash
# Install git hooks for this repository.
# Run once after cloning: bash scripts/install-hooks.sh
set -euo pipefail

HOOKS_DIR=".git/hooks"
SOURCE_DIR="scripts/hooks"

if [ ! -d "$HOOKS_DIR" ]; then
  echo "Error: $HOOKS_DIR not found. Run from the repository root."
  exit 1
fi

for hook in "$SOURCE_DIR"/*; do
  name=$(basename "$hook")
  dest="$HOOKS_DIR/$name"
  cp "$hook" "$dest"
  chmod +x "$dest"
  echo "Installed $dest"
done

echo "Git hooks installed."
