#!/usr/bin/env bash
#
# Run all demos in the example directory.
#
# Each demo must have a run.sh script that handles its own execution.
#
# Usage:
#   ./run_all_demos.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# List of demo directories (relative to SCRIPT_DIR)
DEMOS=(
    "simple_demo"
)

FAILED_DEMOS=()
PASSED_DEMOS=()

echo "Running ${#DEMOS[@]} demo(s)..."
echo ""

for demo in "${DEMOS[@]}"; do
    demo_dir="$SCRIPT_DIR/$demo"

    echo "========================================"
    echo "Running demo: $demo"
    echo "========================================"

    putd "$demo_dir"

    if [[ ! -f "run.sh" ]]; then
        echo "ERROR: $demo_dir/run.sh not found"
        FAILED_DEMOS+=("$demo")
        continue
    fi

    if "./run.sh"; then
        echo "✓ Demo '$demo' passed"
        PASSED_DEMOS+=("$demo")
    else
        echo "✗ Demo '$demo' failed"
        FAILED_DEMOS+=("$demo")
    fi
    popd
    echo ""
done

# Summary
echo "========================================"
echo "Summary"
echo "========================================"
echo "Passed: ${#PASSED_DEMOS[@]}"
for demo in "${PASSED_DEMOS[@]}"; do
    echo "  ✓ $demo"
done

if [[ ${#FAILED_DEMOS[@]} -gt 0 ]]; then
    echo "Failed: ${#FAILED_DEMOS[@]}"
    for demo in "${FAILED_DEMOS[@]}"; do
        echo "  ✗ $demo"
    done
    exit 1
fi

echo ""
echo "All demos passed!"
