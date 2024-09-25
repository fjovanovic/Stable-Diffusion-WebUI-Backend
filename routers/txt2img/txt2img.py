from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse


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
    height: int = Query(
        default=512, 
        enum=[512, 1024], 
        description='The height in pixels of the generated image'
    ),
    width: int = Query(
        default=512, 
        enum=[512, 1024], 
        description='The width in pixels of the generated image'
    ),
    num_inference_steps: int = Query(
        default=50,
        ge=10,
        le=50,
        description='The number of denoising steps. ' \
            'More denoising steps usually lead to a higher ' \
            'quality image at the expense of slower inference'
    ),
    guidance_scale: int = Query(
        default=7.5,
        ge=1,
        le=10,
        description='A higher guidance scale value encourages ' \
            'the model to generate images closely linked ' \
            'to the text prompt at the expense of lower image quality. ' \
            'Guidance scale is enabled when **guidance_scale > 1**'
    ),
    negative_prompt: str = Query(
        default='', 
        description='The prompt or prompts to guide what to ' \
            'not include in image generation. If not defined, ' \
            'you need to pass negative_prompt_embeds instead'
    ),
    num_images_per_prompt: str = Query(
        default=1,
        description='The number of images to generate per prompt'
    )
) -> str:
    
    return JSONResponse(content={'message': 'Hello'})