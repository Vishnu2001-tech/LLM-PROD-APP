from functools import lru_cache
from typing import Union

from fastapi import FastAPI, Depends
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware

# Uncomment and adjust once the routers are created
from routers import todos

import config

app = FastAPI()

# Uncomment and adjust once the router is created
app.include_router(todos.router)

# CORS configuration, needed for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global HTTP exception handler to handle errors
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print(f"{repr(exc)}")
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# To use the settings
@lru_cache()
def get_settings():
    return config.Settings()

@app.get("/")
def read_root(settings: config.Settings = Depends(get_settings)):
    # Print the app_name configuration
    print(settings.app_name)
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}