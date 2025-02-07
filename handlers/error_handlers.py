from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.exceptions import HTTPException


async def not_found_exception_handler(
    request: Request, 
    exc: HTTPException
) -> JSONResponse:
    if exc.detail:
        content = {'error': exc.detail}
    else:
        content = {'error': 'Bad request, check url'}
    
    return JSONResponse(content=content, status_code=404)


async def validation_exception_handler(
    request: Request, 
    exc: RequestValidationError
) -> JSONResponse:
    content = {'error': 'Missing / invalid data'}

    return JSONResponse(content=content, status_code=422)


async def global_exception_handler(
    request: Request, 
    exc: Exception
) -> JSONResponse:
    content = {'error': 'Unexpected error'}
    
    return JSONResponse(content=content, status_code=500)