#!/bin/bash

# Build the API image
docker build -f Dockerfile.api -t whisperx-api:latest .

# Run the container with GPU support
docker run --gpus all -p 8000:8000 -it whisperx-api:latest