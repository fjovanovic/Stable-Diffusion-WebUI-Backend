from fastapi import APIRouter


router = APIRouter(
    prefix='/img2img',
    tags=['Image to image']
)


@router.get(
    path='/generate_images',
    summary='Generate images',
    description='This endpoint allows you to generate images ' \
        'based on input image'
)
async def generate_images():
    ...