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