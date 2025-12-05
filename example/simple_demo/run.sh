#!/usr/bin/env bash
#
# Run the simple_demo example.
#
# Prerequisites:
#   - Docker and Docker Compose installed
#   - Docker images built (run `docker buildx bake` from repository root)
#
# Usage:
#   ./run.sh
#

set -e

# Set up cleanup on exit
cleanup() {
    echo "Cleaning up..."
    docker compose down
}
trap cleanup EXIT

# Start Kafka and wait for it to be healthy
echo "Starting Kafka..."
docker compose up -d kafka

echo "Waiting for Kafka to be healthy..."
if ! timeout 60s bash -c 'until docker compose ps kafka | grep -q "healthy"; do sleep 2; done'; then
    echo "ERROR: Kafka failed to become healthy"
    docker compose logs kafka
    exit 1
fi

echo "Running xppu_frost..."

# Run the application in fast mode (override docker-compose command)
if docker compose run --rm xppu_frost sh -c "python src-gen/Main/Main.py -f true"; then
    echo "Demo ran successfully"
    exit 0
else
    echo "Demo failed"
    docker compose logs xppu_frost
    exit 1
fi
