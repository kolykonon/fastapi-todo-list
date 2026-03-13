from fastapi import FastAPI
from views import tasks_router
import uvicorn

app = FastAPI()

app.include_router(tasks_router)


def start() -> None:
    uvicorn.run("main:app", reload=True)


if __name__ == "__main__":
    start()
