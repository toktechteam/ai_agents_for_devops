#!/bin/bash
set -e

echo " Running AutoGen Free Test..."

python src/run.py | tee output.log

if grep -qi "Analysis" output.log; then
  echo "✅ Test Passed"
else
  echo "❌ Test Failed"
  exit 1
fi
