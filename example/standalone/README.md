# Standalone Example

A minimal standalone example of the xPPU digital twin without external dependencies.

## Overview

This example runs the xPPU simulation in standalone mode, demonstrating the digital twin
functionality without other external libraries. It includes:

- **XPPU**: The complete xPPU digital twin model
- **FrostBus**: Event bus for inter-module communication
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

### 2. Run the example

```bash
cd example/standalone
docker compose up
```

Or use the run script:

```bash
./run.sh
```

## Local Development

### 1. Build and run locally

```bash
lfc src/Main.lf
python src-gen/Main/Main.py -f false
```

The `-f false` flag enables real-time execution (disables fast mode).

## Configuration

### Command Line Options

| Option | Description                | Default |
| ------ | -------------------------- | ------- |
| `-f`   | Fast mode (`true`/`false`) | `true`  |

### Configuration Files

| File                         | Description                   |
| ---------------------------- | ----------------------------- |
| `resources/frost_config.yml` | Frost framework configuration |

## Project Structure

```
standalone/
├── src/
│   └── Main.lf              # Main reactor with XPPU and XPPUScheduler
├── resources/
│   ├── frost_config.yml     # Frost configuration
│   ├── data_model/          # Machine data model definitions
│   ├── scheduling_instances/# Pre-defined scheduling instances
│   └── template/            # Templates for configuration
├── Dockerfile               # Container build instructions
├── docker-compose.yml       # Container setup
├── run.sh                   # Run script
```
