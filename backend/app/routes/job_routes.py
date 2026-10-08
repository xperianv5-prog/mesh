from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Job
from ..deps import current_user

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.get("/{job_id}")
def get_job(
    job_id: str,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    job = db.query(Job).filter(Job.id == job_id, Job.user_id == user.id).first()
    if not job:
        raise HTTPException(404, "Job not found")
    return {
        "id": job.id,
        "status": job.status.value if hasattr(job.status, "value") else job.status,
        "stage": job.stage,
        "progress": job.progress,
        "error": job.error,
        "prompt": job.prompt,
        "quality": job.quality,
    }


@router.get("")
def list_jobs(
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
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
            "created_at": str(j.created_at),
        }
        for j in jobs
    ]
