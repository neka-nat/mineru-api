from fastapi import FastAPI

from .pdf import parse_router

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(parse_router, prefix="/api")
