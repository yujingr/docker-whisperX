import requests
import sys
import json

def transcribe_audio(file_path, api_url="http://localhost:8000/transcribe/"):
    """
    Transcribe audio file using the WhisperX API
    
    Args:
        file_path: Path to audio file
        api_url: URL of the WhisperX API endpoint
    """
    # Prepare the files and data
    files = {
        "file": open(file_path, "rb")
    }
    
    data = {
        "model_name": "large-v2",
        "language": "en",
        "output_format": "json",
        "vad": "true",
        "diarize": "true"
    }
    
    # Send the request
    print(f"Sending request to {api_url}...")
    response = requests.post(api_url, files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print("Transcription successful!")
        print(json.dumps(result, indent=2))
        return result
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_api.py <audio_file_path>")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    transcribe_audio(audio_path) 