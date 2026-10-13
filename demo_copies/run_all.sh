#!/bin/sh
# Verify all demo copies run. Usage: sh demo_copies/run_all.sh
cd "$(dirname "$0")/.." || exit 1
pass=0; fail=0
for f in demo_copies/demo_*.py; do
  printf '%-32s ' "$f"
  if .venv/bin/python "$f" >/tmp/out_$(basename "$f").log 2>&1; then
    echo OK; pass=$((pass+1))
  else
    echo FAIL; fail=$((fail+1))
  fi
done
echo "passed=$pass failed=$fail"
