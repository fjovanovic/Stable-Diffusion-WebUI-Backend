from typing import Dict

from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI(
    title='FastAPI (v1)',
    summary='API endpoints for AI Image Generator WebUI',
    version='0.1.0',
    swagger_ui_parameters={
        'useUnsafeMarkdown': True
    }
)


@app.get(
    path='/ping',
    tags=['Server'],
    summary='Check API server status',
    description='Check if the API server is running'
)
async def ping() -> Dict[str, str]:
    content = {'message': 'pong!'}

    return JSONResponse(content=content)