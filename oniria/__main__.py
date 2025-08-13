import os
import uvicorn
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from oniria.infrastructure.firebase.firebase_config import *
from oniria.application.middlewares import (
    handle_unauthorized,
    UnauthorizedException,
    handle_not_found,
    NotFoundException,
    handle_conflict,
    ConflictException,
    handle_forbidden,
    ForbiddenException,
)
from oniria.infrastructure.db import Base, engine
from oniria.infrastructure.db import RenownDB
from sqlalchemy import text
from sqlalchemy.orm import Session
from oniria.interfaces.routes import router as auth_routes
from oniria.interfaces.cs_routes import router as cs_routes


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
    with Session(engine) as session:
        if session.query(RenownDB).count() == 0:
            load_data()
        else:
            print("Data already loaded, skipping DML execution.")


def load_data():
    sql_file = f"{Path(__file__).resolve().parents[1]}/resources/database/oniria.dml"
    if not os.path.isfile(sql_file):
        print(f"Cannot find DML file: {sql_file}")
        return
    with engine.connect() as connection:
        with open(sql_file, "r", encoding="utf-8") as file:
            sql_script = file.read()
            try:
                connection.execute(text(sql_script))
                connection.commit()
                print("DML loaded successfully.")
            except Exception as e:
                print("Error while loading DML:", e)


origins = json.loads(os.environ["ORIGINS"])


def get_application() -> FastAPI:
    prefix: str = "/oniria"
    app = FastAPI(title="Oniria API")
    app.add_exception_handler(UnauthorizedException, handle_unauthorized)
    app.add_exception_handler(NotFoundException, handle_not_found)
    app.add_exception_handler(ConflictException, handle_conflict)
    app.add_exception_handler(ForbiddenException, handle_forbidden)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(auth_routes, prefix=prefix)
    app.include_router(cs_routes, prefix=prefix)
    return app


app = get_application()


def start():
    create_tables()
    uvicorn.run(
        "oniria.__main__:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("RELOAD", "false").lower() == "true",
    )


def dev():
    create_tables()
    uvicorn.run("oniria.__main__:app", host="0.0.0.0", port=8000, reload=True)


def prod():
    create_tables()
    uvicorn.run("oniria.__main__:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    start()
