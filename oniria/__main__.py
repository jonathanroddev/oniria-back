import os
import uvicorn
from fastapi import FastAPI

from oniria import Base, engine
from oniria.auth.interfaces.routes import router as auth_routes


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")


def get_application() -> FastAPI:
    prefix: str = "/oniria"
    app = FastAPI(title="Oniria API")
    app.include_router(auth_routes, prefix=prefix, tags=["auth"])
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
