from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class JobResponse(BaseModel):
    id: str
    status: str
    stage: str | None = None
    progress: int = 0
    error: str | None = None
    mesh_url: str | None = None
    scene_graph: list | None = None
