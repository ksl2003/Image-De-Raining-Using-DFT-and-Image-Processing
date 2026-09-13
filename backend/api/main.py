from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
from PIL import Image
import io
import base64
from model_utils import remove_rain_fallback
import os

app = FastAPI(title="Image De-raining API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("FastAPI DFT de-raining server started successfully")

@app.get("/")
async def root():
    print("GET / request received")
    return {"message": "Image De-raining API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": False,
        "processing_mode": "dft"
    }

@app.post("/api/derain")
async def derain_image(file: UploadFile = File(...)):
    """
    Process a rainy image and return the de-rained version
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        rainy_np = np.array(image, dtype=np.float32) / 255.0
        clean_pred = remove_rain_fallback(rainy_np)
        processing_mode = "dft"
        
        # Convert to PIL Image
        clean_img = (clean_pred * 255).astype(np.uint8)
        clean_pil = Image.fromarray(clean_img)
        
        # Convert to base64
        buffer = io.BytesIO()
        clean_pil.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Also encode original for comparison
        buffer_orig = io.BytesIO()
        image.save(buffer_orig, format='PNG')
        orig_base64 = base64.b64encode(buffer_orig.getvalue()).decode('utf-8')
        
        return JSONResponse({
            "success": True,
            "original_image": f"data:image/png;base64,{orig_base64}",
            "derained_image": f"data:image/png;base64,{img_base64}",
            "processing_mode": processing_mode,
            "message": "Image processed successfully"
        })
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

