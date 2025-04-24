# Custom name for your image and container
$IMAGE_NAME = "whisperx-api"
$IMAGE_TAG = "latest"
$CONTAINER_NAME = "whisperx-api-container"

# Build the API image using the wheels approach
docker build -f Dockerfile.api.wheels -t ${IMAGE_NAME}:${IMAGE_TAG} .

# Run the container with GPU support and custom name
docker run --gpus all -p 8000:8000 --name ${CONTAINER_NAME} -it ${IMAGE_NAME}:${IMAGE_TAG} 