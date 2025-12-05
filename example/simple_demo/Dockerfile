FROM xppu-frost-base AS builder

# Copy src files
COPY src /app/src

# Build the project
RUN lfc src/Main.lf

# Install additional runtime dependencies
RUN /venv/bin/pip install -r /opt/xppu-frost/requirements.txt

# Runtime image
FROM python:3.13-alpine3.21

COPY --from=builder /venv /venv
COPY --from=builder /app/src-gen /app/src-gen
COPY resources /app/resources

WORKDIR /app
ENV PATH="/venv/bin:$PATH"

CMD ["python", "src-gen/Main/Main.py"]
