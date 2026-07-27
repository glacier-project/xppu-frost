FROM xppu-frost-base AS builder

WORKDIR /opt/xppu-frost/example/simple_demo

# Install additional runtime dependencies
COPY requirements.txt /opt/xppu-frost/example/simple_demo/requirements.txt
RUN /venv/bin/pip install -r /opt/xppu-frost/example/simple_demo/requirements.txt

# Copy src files
COPY src /opt/xppu-frost/example/simple_demo/src

# Build the project
RUN lfc src/Main.lf

# Runtime image
FROM python:3.12-slim AS runtime

COPY --from=builder /venv /venv
COPY --from=builder /opt/xppu-frost/example/simple_demo/src-gen /opt/xppu-frost/example/simple_demo/src-gen
COPY --from=builder /opt/xppu-frost/resources /opt/xppu-frost/resources
COPY resources /opt/xppu-frost/example/simple_demo/resources

WORKDIR /opt/xppu-frost/example/simple_demo
ENV PATH="/venv/bin:$PATH"

CMD ["python", "src-gen/Main/Main.py"]
