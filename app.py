import os, io
from typing import Literal
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import httpx

load_dotenv()
app = FastAPI(title="DI-Ai-Studio API", docs_url=None, redoc_url=None)

class GenerateBody(BaseModel):
    prompt: str = Field(min_length=5, max_length=2000)
    tier: Literal["community", "premium"] = "community"
    aspect_ratio: Literal["9:16", "16:9", "1:1"] = "16:9"
    duration_seconds: int = Field(default=5, ge=3, le=10)
    camera_motion: str = "Auto"
    outputs: int = Field(default=1, ge=1, le=4)

@app.get("/health")
def health():
    return {"app": "DI-Ai-Studio", "status": "ok", "authentication": "disabled"}

@app.post("/video/generate")
async def generate(body: GenerateBody):
    if body.tier == "community":
        hf_token = os.getenv("HF_TOKEN", "")
        if not hf_token:
            raise HTTPException(503, "Community provider is not configured. Add HF_TOKEN on the backend.")
        from huggingface_hub import InferenceClient
        try:
            client = InferenceClient(provider=os.getenv("HF_PROVIDER", "fal-ai"), api_key=hf_token)
            video = client.text_to_video(body.prompt, model=os.getenv("HF_MODEL", "tencent/HunyuanVideo"),
                num_frames=max(24, body.duration_seconds * 8))
            data = video if isinstance(video, bytes) else bytes(video)
        except Exception as e:
            raise HTTPException(502, f"Community generation failed: {str(e)[:300]}")
    else:
        token = os.getenv("REPLICATE_API_TOKEN", "")
        model = os.getenv("REPLICATE_MODEL", "")
        if not token or not model:
            raise HTTPException(503, "Premium provider is not configured on the backend.")
        async with httpx.AsyncClient(timeout=240) as client:
            try:
                response = await client.post(f"https://api.replicate.com/v1/models/{model}/predictions",
                    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Prefer": "wait=60"},
                    json={"input": {"prompt": body.prompt, "aspect_ratio": body.aspect_ratio,
                        "duration": body.duration_seconds, "camera_motion": body.camera_motion}})
                response.raise_for_status()
                result = response.json()
                output = result.get("output")
                if isinstance(output, list): output = output[0] if output else None
                if not isinstance(output, str) or not output.startswith("http"):
                    raise HTTPException(504, "Prediction is still running or model output format differs; configure polling for this model.")
                file_response = await client.get(output)
                file_response.raise_for_status()
                data = file_response.content
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(502, f"Premium generation failed: {str(e)[:300]}")
    return StreamingResponse(io.BytesIO(data), media_type="video/mp4",
        headers={"Content-Disposition": 'attachment; filename="dan-ai-video.mp4"'})
