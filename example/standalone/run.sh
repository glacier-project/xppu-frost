#!/usr/bin/env bash
#
# Run the standalone example.
#
# Prerequisites:
#   - Docker and Docker Compose installed
#   - Docker images built (run `docker buildx bake` from repository root)
#
# Usage:
#   ./run.sh
#

set -e

echo "Running xppu-frost-standalone..."

# Run the application in fast mode (suppress output on success)
output=$(docker compose run --rm xppu-frost-standalone sh -c "python src-gen/Main/Main.py -f true" 2>&1) && exit_code=0 || exit_code=$?

if [[ $exit_code -eq 0 ]]; then
    echo "Standalone demo ran successfully"
    exit 0
else
    echo "Standalone demo failed"
    echo "$output"
    docker compose logs xppu-frost-standalone
    exit 1
fi
