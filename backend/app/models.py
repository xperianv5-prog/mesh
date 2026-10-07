import enum, time, uuid
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from .database import Base

class JobStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))
    jobs = relationship("Job", back_populates="user")

class Job(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
    stage = Column(String, nullable=True)
    progress = Column(Integer, default=0)
    image_key = Column(String)
    mesh_key = Column(String, nullable=True)
    prompt = Column(String, default="object")
    quality = Column(String, default="balanced")
    scene_graph = Column(JSON, nullable=True)
    error = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))
    user = relationship("User", back_populates="jobs")