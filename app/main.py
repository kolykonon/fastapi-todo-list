from fastapi import FastAPI
from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.tasks import router as tasks_router
import uvicorn

app = FastAPI()

app.include_router(tasks_router)
app.include_router(auth_router)


def start() -> None:
    uvicorn.run("main:app", reload=True)


if __name__ == "__main__":
    start()
