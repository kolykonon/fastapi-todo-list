from fastapi import FastAPI
from api import tasks_router, auth_router
import uvicorn

app = FastAPI()

app.include_router(tasks_router)
app.include_router(auth_router)


def start() -> None:
    uvicorn.run("main:app", reload=True)


if __name__ == "__main__":
    start()
