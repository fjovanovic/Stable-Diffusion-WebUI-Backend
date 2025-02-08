import io

from PIL import Image
from fastapi import (
    Form,
    APIRouter, 
    UploadFile, 
    File 
)
from fastapi.responses import StreamingResponse
import torch
from diffusers import AutoPipelineForImage2Image


router = APIRouter(
    prefix='/img2img',
    tags=['Image to image']
)


img2img_active_model = ''
img2img_pipe = None


@router.post('/img2img/generate_image')
async def img2img_generate_image(
    model: str = Form(
        default='stabilityai/stable-diffusion-xl-base-1.0',
        description='Name of the pretrained model'
    ),
    prompt: str = Form(
        description='The prompt or prompts to guide image generation'
    ),
    negative_prompt: str = Form(
        default='',
        description='The prompt or prompts to guide what to not include in image generation'
    ),
    file: UploadFile = File(
        description='Input image based on which the output will be generated'
    )
) -> StreamingResponse:
    contents = await file.read()
    input_image = Image.open(io.BytesIO(contents))
    global img2img_active_model, img2img_pipe

    if img2img_active_model != model:
        img2img_pipe = AutoPipelineForImage2Image.from_pretrained(
            model,
            torch_dtype=torch.float16,
            variant='fp16'
        )
        img2img_pipe.to('cuda')
        img2img_active_model = model


    image = img2img_pipe(
        prompt,
        image=input_image,
        negative_prompt=negative_prompt
    ).images[0]

    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type='image/png',
    )