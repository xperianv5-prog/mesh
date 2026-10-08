import io
import uuid
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from PIL import Image
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Job, JobStatus
from ..deps import current_user
from ..storage import storage

router = APIRouter(prefix="/api", tags=["upload"])


@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    prompt: str = Form("object"),
    quality: str = Form("balanced"),
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    data = await file.read()
    img = Image.open(io.BytesIO(data)).convert("RGB")
    if img.width * img.height > 20_000_000:
        raise HTTPException(400, "Image too large (max 20MP)")

    image_key = f"uploads/{uuid.uuid4()}.png"
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    storage.upload_bytes(buf.getvalue(), image_key, "image/png")

    job = Job(
        id=str(uuid.uuid4()),
        user_id=user.id,
        status=JobStatus.PENDING,
        image_key=image_key,
        prompt=prompt,
        quality=quality,
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    return {
        "job_id": job.id,
        "status": "queued",
        "message": "Image uploaded successfully",
        "image_key": image_key,
    }
