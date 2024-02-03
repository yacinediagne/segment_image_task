
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from fastapi import FastAPI, File, UploadFile

import os

import io

import numpy as np

import torch

from mobile_sam import SamAutomaticMaskGenerator, SamPredictor, sam_model_registry

from PIL import Image

from tools import format_results, point_prompt, fast_process

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

sam_checkpoint = "./mobile_sam.pt"
model_type = "vit_t"

mobile_sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
mobile_sam = mobile_sam.to(device=device)
mobile_sam.eval()

mask_generator = SamAutomaticMaskGenerator(mobile_sam)
predictor = SamPredictor(mobile_sam)

app = FastAPI()


# @app.post("/files/")
# async def create_file(file: Annotated[bytes, File()]):
#     return {"file_size": len(file)}

def segment_everything(
    image,
    input_size=1024,
    better_quality=False,
    withContours=True,
    use_retina=True,
    mask_random_color=True,
):
    global mask_generator

    input_size = int(input_size)
    w, h = image.size
    scale = input_size / max(w, h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    image = image.resize((new_w, new_h))

    nd_image = np.array(image)
    annotations = mask_generator.generate(nd_image)

    fig = fast_process(
        annotations=annotations,
        image=image,
        device=device,
        scale=(1024 // input_size),
        better_quality=better_quality,
        mask_random_color=mask_random_color,
        bbox=None,
        use_retina=use_retina,
        withContours=withContours,
    )
    return fig

@app.post("/segment-image")
async def create_upload_file(file: UploadFile= File(...) ):
    file= await file.read()
    image = Image.open(io.BytesIO(file)).convert("RGB")
    image_seg= segment_everything(image=image)
    path = "generated/result.png"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    image_seg.save(path)
    return FileResponse(path, media_type="image/jpeg")
    



