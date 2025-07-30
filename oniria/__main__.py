import os
import uvicorn
from fastapi import FastAPI
from pathlib import Path

from oniria.db import Base, engine
from oniria.campaign.infrastructure.db import Renown
from sqlalchemy import text
from sqlalchemy.orm import Session
from oniria.auth.interfaces.routes import router as auth_routes


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
    with Session(engine) as session:
        if session.query(Renown).count() == 0:
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


def get_application() -> FastAPI:
    prefix: str = "/oniria"
    app = FastAPI(title="Oniria API")
    app.include_router(auth_routes, prefix=prefix)
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
