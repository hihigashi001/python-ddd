import uvicorn
from fastapi import FastAPI
from web import message_controller

app = FastAPI()

app.include_router(message_controller.router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)