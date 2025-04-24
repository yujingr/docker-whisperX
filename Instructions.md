Originial:https://github.com/m-bain/whisperX/
Docker: https://github.com/jim60105/docker-whisperX/
Modified Here with FastAPI

1. Git clone the Docker repo
2. Build the Docker image with the following command:
   docker build --build-arg LANG="en zh" --build-arg WHISPER_MODEL=large-v2 -t whisperx:large-v2-en-zh .

3. Wrap the Docker container with FastAPI and build the FastAPI app with the wheels version

docker build -f Dockerfile.api.wheels -t whisperx-api:latest .

4. Run the FastAPI app container with the following command:
   docker run --gpus all -p 8000:8000 -it whisperx-api:latest
