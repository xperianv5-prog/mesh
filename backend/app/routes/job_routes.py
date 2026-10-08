from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Job
from ..deps import current_user
from ..storage import storage

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.get("/{job_id}")
def get_job(job_id: str, user: User = Depends(current_user), db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id, Job.user_id == user.id).first()
    if not job:
        raise HTTPException(404, "Job not found")

    mesh_url = storage.presigned_url(job.mesh_key) if job.mesh_key else None

    return {
        "id": job.id,
        "status": job.status.value if hasattr(job.status, "value") else job.status,
        "stage": job.stage,
        "progress": job.progress,
        "error": job.error,
        "mesh_url": mesh_url,
        "prompt": job.prompt,
        "quality": job.quality,
    }


@router.get("")
def list_jobs(user: User = Depends(current_user), db: Session = Depends(get_db)):
    jobs = (
        db.query(Job)
        .filter(Job.user_id == user.id)
        .order_by(Job.created_at.desc())
        .limit(50)
        .all()
    )
    return [
        {
            "id": j.id,
            "status": j.status.value if hasattr(j.status, "value") else j.status,
            "stage": j.stage,
            "progress": j.progress,
            "mesh_url": storage.presigned_url(j.mesh_key) if j.mesh_key else None,
            "created_at": str(j.created_at),
        }
        for j in jobs
    ]
