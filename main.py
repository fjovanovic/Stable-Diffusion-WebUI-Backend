from typing import Dict

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException

from handlers import (
    not_found_exception_handler,
    validation_exception_handler,
    global_exception_handler
)


app = FastAPI(
    title='FastAPI (v1)',
    summary='API endpoints for AI Image Generator WebUI',
    version='0.1.0',
    swagger_ui_parameters={
        'useUnsafeMarkdown': True
    }
)


app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, not_found_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.get(
    path='/ping',
    tags=['Server'],
    summary='Check API server status',
    description='Check if the API server is running'
)
async def ping() -> Dict[str, str]:
    content = {'message': 'pong!'}

    return JSONResponse(content=content)