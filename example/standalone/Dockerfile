FROM xppu-frost-base AS builder

WORKDIR /opt/xppu-frost/example/standalone

# Copy src files
COPY src /opt/xppu-frost/example/standalone/src

# Build the project
RUN lfc src/Main.lf

# Runtime image
FROM python:3.12-slim AS runtime

COPY --from=builder /venv /venv
COPY --from=builder /opt/xppu-frost/example/standalone/src-gen /opt/xppu-frost/example/standalone/src-gen
COPY --from=builder /opt/xppu-frost/resources /opt/xppu-frost/resources
COPY resources /opt/xppu-frost/example/standalone/resources

WORKDIR /opt/xppu-frost/example/standalone
ENV PATH="/venv/bin:$PATH"

CMD ["python", "src-gen/Main/Main.py"]
