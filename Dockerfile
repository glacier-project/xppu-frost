# Base image for building xppu-frost projects
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git gcc g++ make cmake curl openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Install Lingua Franca compiler (lfc)
RUN curl -Ls https://install.lf-lang.org | bash -s cli && \
    ln -s /root/.local/bin/lfc /usr/local/bin/lfc

# Setup Python environment
RUN pip install --upgrade pip && pip install virtualenv && python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy frost framework and xppu sources
COPY frost /opt/xppu-frost/frost
COPY src /opt/xppu-frost/src
COPY resources /opt/xppu-frost/resources
COPY requirements.txt /opt/xppu-frost/requirements.txt

# Install dependencies
RUN /venv/bin/pip install -r /opt/xppu-frost/requirements.txt

WORKDIR /app
