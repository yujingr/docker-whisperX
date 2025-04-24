# Build the API image using the wheels approach
docker build -f Dockerfile.api.wheels -t whisperx-api:latest .

# Run the container with GPU support
docker run --gpus all -p 8000:8000 -it whisperx-api:latest 