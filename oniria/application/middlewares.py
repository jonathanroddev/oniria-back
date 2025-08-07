from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from oniria.domain import (
    NotFoundException,
    ConflictException,
    UnauthorizedException,
    ForbiddenException,
)


async def handle_not_found(request: Request, exc: NotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
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


async def handle_forbidden(request: Request, exc: ForbiddenException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=jsonable_encoder({"detail": str(exc)}),
    )
