// Docker Bake configuration for xppu-frost
// Usage: docker buildx bake [target]
// Examples:
//   docker buildx bake base         # Build base image only
//   docker buildx bake simple_demo  # Build simple_demo (and base if needed)
//   docker buildx bake              # Build all targets
//
// With docker-compose (builds and runs):
//   docker buildx bake && cd example/simple_demo && docker compose up

group "default" {
  targets = ["base", "simple_demo"]
}

target "base" {
  context    = "."
  dockerfile = "Dockerfile"
  tags       = ["xppu-frost-base:latest"]
}

target "simple_demo" {
  context    = "example/simple_demo"
  dockerfile = "Dockerfile"
  tags       = ["xppu-frost-demo:latest"]
  contexts   = {
    xppu-frost-base = "target:base"
  }
}
