from fastapi import APIRouter, Query


router = APIRouter(
    prefix='/txt2img',
    tags=['Text to image']
)


@router.get(
    path='/generate_images',
    summary='Generate images',
    description='This endpoint allows you to generate images ' \
        'based on prompt and other parameters'
)
async def generate_images(
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
    )
):
    ...