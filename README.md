# xPPU-Frost

A digital twin implementation of the Extended Pick&Place Unit (xPPU) using the [Frost](https://github.com/glacier-project/frost) framework and [Lingua Franca](https://www.lf-lang.org/).

![xPPU Diagram](docs/images/xppu.png)

## Overview

This repository contains a virtual platform for simulating and testing the **xPPU (Extended Pick&Place Unit)**, a Cyber-Physical Production System (CPPS) used as a benchmark in Industry 4.0 research. The xPPU is a modular manufacturing demonstrator that simulates a real-world production line for picking, processing, and sorting workpieces.

The implementation leverages the Frost framework to provide:

- **Deterministic execution** of the xPPU control logic
- **Digital Twin capabilities** for virtual testing and validation
- **Modular architecture** with reusable components (Stack, Crane, Stamp, Conveyor)
- **Data model-driven interface** for flexible machine configuration
- **Kafka integration** for real-time data streaming

### Frost Framework

[Frost](https://github.com/glacier-project/frost) is the core simulation platform of the GLACIER ecosystem, enabling the development and testing of Cyber-Physical Production Systems (CPPS). It allows users to build high-fidelity digital twins that replicate the Application Programming Interfaces (APIs) of real production systems, streamlining the process of adapting and deploying prototype software to physical hardware.

### Machine Data Model

The [Machine Data Model](https://github.com/esd-univr/machine-data-model) defines the interface between the machine and other platform components. Inspired by the OPC UA Information Model, it uses a tree-like structure to organize:

- **Variables**: Sensors, actuators, and state information
- **Methods**: Asynchronous commands and operations
- **Folders**: Hierarchical organization of components

## xPPU Components

The xPPU consists of the following main modules:

| Component      | Description                                                    |
| -------------- | -------------------------------------------------------------- |
| **Stack**      | Workpiece storage and dispensing unit with monostable cylinder |
| **Crane**      | Rotary crane for workpiece transport with pneumatic gripper    |
| **Stamp**      | Stamping station for workpiece processing                      |
| **LSConveyor** | Linear sorting conveyor with position sensors                  |

More details about each component can be found in the `src/` directory.

## Prerequisites

- Python 3.12 or higher
- [Lingua Franca](https://www.lf-lang.org/) compiler (`lfc`) 0.9.0+ - [Installation guide](https://www.lf-lang.org/docs/installation)
- CMake 3.20+ (for building)
- Docker 20.10+ (optional, for containerized deployment)

## Getting Started

### 1. Clone the repository

```bash
git clone --recursive https://github.com/glacier-project/xppu-frost.git
cd xppu-frost
```

> **Note:** The `--recursive` flag is required to clone the Frost submodule.

### 2. Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### 3. Verify setup

```bash
cd test
make test-TestStack
```

## Project Structure

The main source code is in `src/`, with each xPPU component in its own folder. The `frost/` submodule contains the simulation framework. Tests are in `test/` with their configurations in `test/resources/`. The `example/` folder contains ready-to-run demos. The `resources/` folder contains the data model definitions that describe the xPPU interface (variables, methods, folder structure).

```
xppu-frost/
├── src/
│   ├── XPPU.lf                 # xPPU composite reactor
│   ├── common/                 # Shared components (MonostableCylinder, etc.)
│   ├── stack/                  # Stack module
│   ├── crane/                  # Crane module
│   ├── stamp/                  # Stamp module
│   ├── conveyor/               # Conveyor module
│   └── python-lib/             # Python utilities
├── example/
│   └── simple_demo/            # Simple demo with Kafka integration
├── test/                       # Test suite
│   ├── src/                    # Test reactors
│   └── resources/              # Test configurations
├── resources/
│   └── data_model/             # Data model definitions
├── frost/                      # Frost framework (submodule)
├── Dockerfile                  # Base Docker image
└── docker-bake.hcl             # Docker Bake configuration
```

## Running Examples

### Simple Demo (with Kafka)

The simple demo showcases the xPPU with Kafka integration for data streaming:

```bash
cd example/simple_demo

# Install dependencies
python -m pip install -r requirements.txt

# Start Kafka (using Docker Compose)
docker compose up -d kafka

# Build and run the demo
lfc src/Main.lf
./bin/Main -f false  # -f false for real-time execution
```

To run entirely in Docker:

```bash
# Build all images
docker buildx bake

# Run the demo
cd example/simple_demo
docker compose up
```

## Running Tests

```bash
cd test

# Run all tests
make all

# Run a specific test
make test-TestStack
```

## Configuration

### Frost Configuration

The `resources/frost_config.yml` file configures reactor parameters and logging:

```yaml
time_precision: MSECS      # Time precision for logs (SECS, MSECS, USECS, NSECS)
logging_level: INFO        # Global logging level (DEBUG, INFO, WARNING, ERROR)

reactors:
  xppu:
    logging_level: DEBUG   # Per-reactor logging override
    parameters:
      data_model_path: "resources/data_model/xppu.yml"
```

### Data Model

The xPPU data model is defined in YAML files under [`resources/data_model/`](resources/data_model/xppu.yml). It specifies:

- Variables (state, sensors, actuators)
- Methods (commands, operations)
- Hierarchical folder structure

## Docker Support

### Building Images

Using Docker Bake:

```bash
# Build all images
docker buildx bake

# Build specific target
docker buildx bake base
docker buildx bake simple_demo
```

### Running in Docker

```bash
docker run --rm xppu-frost-demo:latest
```

## References

- [Lingua Franca Documentation](https://www.lf-lang.org/docs)
- [Frost Framework](https://github.com/glacier-project/frost)
- [Machine Data Model](https://github.com/esd-univr/machine-data-model)
- [Glacier Project](https://github.com/glacier-project)
- [xPPU @ TUM](https://www.mec.ed.tum.de/ais/forschung/demonstratoren/ppu/)

## Contributing

Contributions are welcome! Please follow the [contribution guidelines](.github/copilot-instructions.md) for coding style and commit conventions.

## License

See [LICENSE](LICENSE) file for details.
