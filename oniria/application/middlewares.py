from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from oniria.domain import NoContentException, ConflictException, UnauthorizedException


async def handle_no_content(request: Request, exc: NoContentException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content=jsonable_encoder({"detail": str(exc)}),
    )


async def handle_conflict(request: Request, exc: ConflictException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=jsonable_encoder({"detail": str(exc)}),
    )


async def handle_unauthorized(
    request: Request, exc: UnauthorizedException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder({"detail": str(exc)}),
    )
