# Simple Demo

A demonstration of the xPPU digital twin with Kafka integration for real-time data streaming.

## Overview

This example runs the xPPU simulation and streams variable updates to a Kafka topic (`xppu_data`). It includes:

- **KafkaProducer**: Subscribes to xPPU variables and publishes updates to Kafka
- **XPPUScheduler**: Manages workpiece processing through the xPPU modules

## Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)
- Lingua Franca compiler (`lfc`)

## Quick Start (Docker)

### 1. Build the images

From the repository root:

```bash
docker buildx bake
```

### 2. Run the demo

```bash
cd example/simple_demo
docker compose up
```

This starts:

- **Kafka**: Message broker on ports 9092 (internal) and 9093 (host)
- **xppu_frost**: The xPPU simulation connected to Kafka

### 3. Consume messages (optional)

In another terminal:

```bash
source .venv/bin/activate
cd example/simple_demo
python test/consumer.py
```

## Local Development

### 1. Start Kafka only

```bash
docker compose up -d kafka
```

### 2. Build and run locally

```bash
lfc src/Main.lf
./bin/Main -f false
```

The `-f false` flag enables real-time execution (disables fast mode).

## Configuration

### Environment Variables

| Variable                  | Description               | Default                                            |
| ------------------------- | ------------------------- | -------------------------------------------------- |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka broker address      | `localhost:9093` (host) / `kafka:9092` (container) |
| `FROST_CONFIG`            | Path to Frost config file | `resources/frost_config.yml`                       |

### Kafka Topics

| Topic       | Description                         |
| ----------- | ----------------------------------- |
| `xppu_data` | xPPU variable updates (JSON format) |

## Project Structure

```
simple_demo/
├── src/
│   └── Main.lf              # Main reactor with KafkaProducer and XPPUScheduler
├── resources/
│   └── frost_config.yml     # Frost configuration
├── test/
│   └── consumer.py          # Sample Kafka consumer
├── Dockerfile               # Container build instructions
├── docker-compose.yml       # Multi-container setup
└── requirements.txt         # Python dependencies
```
