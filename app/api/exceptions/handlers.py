from fastapi import Request
from fastapi.responses import JSONResponse

from app.api.exceptions.base import AppError


async def http_base_exception_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )