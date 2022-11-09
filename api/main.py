from fastapi import FastAPI

from routers import categories, clues

app = FastAPI()

app.include_router(categories.router)
app.include_router(clues.router)
