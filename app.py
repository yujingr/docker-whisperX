from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import os
import tempfile
import shutil
from typing import Optional
import whisperx
import torch
import gc

app = FastAPI(title="WhisperX API")

@app.get("/")
def read_root():
    return {"message": "WhisperX API is running"}

@app.post("/transcribe/")
async def transcribe_audio(
    file: UploadFile = File(...),
    model_name: str = Form("large-v2"),
    language: Optional[str] = Form(None),
    batch_size: int = Form(16),
    compute_type: str = Form("float16"),
    output_format: Optional[str] = Form("json"),
    diarize: bool = Form(False),
    min_speakers: Optional[int] = Form(None),
    max_speakers: Optional[int] = Form(None)
):
    # Create a unique temporary directory
    temp_dir = tempfile.mkdtemp()
    try:
        # Save uploaded file
        file_location = os.path.join(temp_dir, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Set device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # 1. Transcribe with whisperx
        model = whisperx.load_model(model_name, device, compute_type=compute_type, language=language)
        audio = whisperx.load_audio(file_location)
        result = model.transcribe(audio, batch_size=batch_size)
        
        # Free up GPU memory
        del model
        gc.collect()
        torch.cuda.empty_cache() if torch.cuda.is_available() else None
        
        # 2. Align whisper output
        language_code = result["language"]
        model_a, metadata = whisperx.load_align_model(language_code=language_code, device=device)
        result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
        
        # Free up GPU memory
        del model_a
        gc.collect()
        torch.cuda.empty_cache() if torch.cuda.is_available() else None
        
        # 3. Assign speaker labels if diarization is requested
        if diarize:
            diarize_model = whisperx.DiarizationPipeline(use_auth_token=None, device=device)
            diarize_segments = diarize_model(
                audio, 
                min_speakers=min_speakers, 
                max_speakers=max_speakers
            )
            result = whisperx.assign_word_speakers(diarize_segments, result)
            
            # Free up GPU memory
            del diarize_model
            gc.collect()
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
            
        # Process output format
        if output_format.lower() == "srt":
            # Convert to SRT format
            srt_content = whisperx.output_to_srt(result)
            return JSONResponse(content={"format": "srt", "content": srt_content})
        
        return JSONResponse(content={"format": "json", "result": result})

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
    finally:
        # Clean up
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)