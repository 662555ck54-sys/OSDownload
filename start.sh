#!/bin/sh
set -eu

BASE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$BASE_DIR/app/main.py" "$@"
fi

if command -v python >/dev/null 2>&1; then
  exec python "$BASE_DIR/app/main.py" "$@"
fi

echo "Python 3.10+ is required."
echo "Download it from: https://www.python.org/downloads/"
exit 1