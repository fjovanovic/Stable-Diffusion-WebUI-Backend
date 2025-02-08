import io
import zipfile

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
import torch
from diffusers import (
    DiffusionPipeline,
    DDIMScheduler,
    PNDMScheduler,
    EulerDiscreteScheduler,
    LMSDiscreteScheduler,
    DPMSolverMultistepScheduler
)


router = APIRouter(
    prefix='/txt2img',
    tags=['Text to image']
)


txt2img_active_model = ''
txt2img_pipe = None
txt2img_active_scheduler = ''
txt2img_available_schedulers = {
    'DDIM': DDIMScheduler,
    'PLMS': PNDMScheduler,
    'Euler': EulerDiscreteScheduler,
    'LMS': LMSDiscreteScheduler,
    'DPM-Solver': DPMSolverMultistepScheduler
}


@router.get(
    path='/txt2img/generate_images',
    summary='Generate images',
    description='This endpoint allows you to generate images ' \
        'based on prompt and other parameters'
)
async def txt2img_generate_images(
    model: str = Query(
        default='stabilityai/stable-diffusion-xl-base-1.0',
        description='One of the pretrained models'
    ),
    prompt: str = Query(
        description='The prompt or prompts to guide image generation'
    ),
    negative_prompt: str = Query(
        default='',
        description='The prompt or prompts to guide what to not include in image generation'
    ),
    scheduler: str = Query(
        default='DPM-Solver',
        enum=[
            'DDIM',
            'PLMS',
            'Euler',
            'LMS',
            'DPM-Solver'
        ],
        description='A scheduler to be used in combination with unet to denoise the encoded image latents'
    ),
    num_of_images: int = Query(
        default=4,
        ge=1,
        le=4,
        description='The number of images to generate per prompt'
    ),
    seed: int = Query(
        description='Number to make generation deterministic'
    ),
    width: int = Query(
        default=512,
        ge=512,
        le=1024,
        description='The width in pixels of the generated image'
    ),
    height: int = Query(
        default=512,
        ge=512,
        le=1024,
        description='The height in pixels of the generated image'
    ),
    inference_steps: int = Query(
        default=50,
        ge=10,
        le=50,
        description='The number of denoising steps. ' \
            'More denoising steps usually lead to a higher ' \
            'quality image at the expense of slower inference'
    ),
    cfg_scale: float = Query(
        default=7.5,
        ge=1,
        le=10,
        description='A higher guidance scale value encourages ' \
            'the model to generate images closely linked ' \
            'to the text prompt at the expense of lower image quality. ' \
            'Guidance scale is enabled when **guidance_scale > 1**'
    ),
    run_on: str = Query(
        default='GPU',
        enum=[
            'GPU',
            'CPU'
        ],
        description='Where the model will run'
    )
) -> StreamingResponse:
    global txt2img_active_model, txt2img_pipe, txt2img_active_scheduler

    if model != txt2img_active_model:
        if txt2img_active_scheduler != scheduler:
            scheduler_model = txt2img_available_schedulers[scheduler].from_pretrained(
                model,
                subfolder='scheduler'
            )
            txt2img_active_scheduler = scheduler

        txt2img_pipe = DiffusionPipeline.from_pretrained(
            model,
            scheduler=scheduler_model,
            torch_dtype=torch.float16,
            use_safetensors=True,
            variant='fp16'
        )

        if run_on == 'GPU':
            txt2img_pipe.to('cuda')
        else:
            txt2img_pipe.enable_model_cpu_offload()
        txt2img_active_model = model

    images = txt2img_pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_images_per_prompt=num_of_images,
        seed=torch.manual_seed(seed),
        num_inference_steps=inference_steps,
        guidance_scale=cfg_scale,
        height=height,
        width=width
    ).images

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for (i, image) in enumerate(images):
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            zipf.writestr(f'image_{i}.png', img_byte_arr.read())

    zip_buffer.seek(0)

    headers = {
        'Content-Disposition': 'attachment; filename=generated_images.zip'
    }

    return StreamingResponse(
        content=zip_buffer,
        status_code=200,
        media_type='application/zip',
        headers=headers
    )