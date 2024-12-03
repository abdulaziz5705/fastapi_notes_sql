from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .routers import users, notes

app = FastAPI()


@app.get("/", tags=["main"])
async def root():
    return RedirectResponse(url="/docs")

app.include_router(users.router)
app.include_router(notes.router)

