# Base image for building xppu-frost projects
FROM python:3.13-alpine3.21

# Install system dependencies (including Qt for PyQt)
RUN apk add --update --no-cache \
    git gcc g++ libc-dev make cmake python3-dev zlib-dev curl bash openjdk17-jre

# Install Lingua Franca compiler (lfc)
RUN curl -Ls https://install.lf-lang.org | bash -s cli && \
    ln -s ~/.local/bin/lfc /usr/local/bin/lfc

# Setup Python environment
RUN pip install --upgrade pip && pip install virtualenv && python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy frost framework and xppu sources
COPY frost /opt/xppu-frost/frost
COPY src /opt/xppu-frost/src
COPY requirements.txt /opt/xppu-frost/requirements.txt

# Install dependencies
RUN /venv/bin/pip install -r /opt/xppu-frost/requirements.txt

WORKDIR /app
