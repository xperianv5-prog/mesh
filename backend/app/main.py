from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import Base, engine
from .routes.auth_routes import router as auth_router
from .routes.upload_routes import router as upload_router
from .routes.job_routes import router as job_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="2D->3D Mesh API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://xperianv5-prog.github.io",
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_origin_regex=r"https://.*\.app\.github\.dev",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(job_router)


@app.get("/health")
def health():
    return {"status": "ok", "message": "mesh backend is running"}


@app.get("/")
def root():
    return {"status": "ok", "service": "mesh backend", "docs": "/docs"}
