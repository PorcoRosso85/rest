#!/bin/bash
# This script runs pytest on all changed files in the git index

set -e

CHANGED_FILES=$(git diff --cached --name-only --diff-filter=ACMR | grep '\.py$')

if [ -n "$CHANGED_FILES" ]; then
    pytest $CHANGED_FILES
fi