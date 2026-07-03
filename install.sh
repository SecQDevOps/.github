#!/bin/sh
# QNODE workspace bootstrapper.
#
#   curl -fsSL https://raw.githubusercontent.com/SecQDevOps/.github/main/install.sh | sh
#
# Creates the QNODE workspace, clones the private harness carrier, and runs its
# bootstrap (ensure uv is installed -> extract harness -> clone every repo as a
# sibling -> print the initial agent prompt). Overridable via environment:
#   QNODE_DIR       target workspace directory        (default: QNODE)
#   QNODE_GIT_BASE  git remote base for the org       (default: git@github.com:SecQDevOps)
set -eu

QNODE_DIR="${QNODE_DIR:-QNODE}"
GIT_BASE="${QNODE_GIT_BASE:-git@github.com:SecQDevOps}"

command -v git  >/dev/null 2>&1 || { echo "error: git is required"  >&2; exit 1; }
command -v make >/dev/null 2>&1 || { echo "error: make is required" >&2; exit 1; }

echo ">> workspace: $QNODE_DIR"
mkdir -p "$QNODE_DIR"
cd "$QNODE_DIR"

if [ -d .github-private/.git ]; then
	echo ">> updating .github-private"
	git -C .github-private pull --ff-only
else
	echo ">> cloning .github-private"
	git clone "$GIT_BASE/.github-private.git"
fi

echo ">> running harness bootstrap"
make -C .github-private ORG="$GIT_BASE" bootstrap
