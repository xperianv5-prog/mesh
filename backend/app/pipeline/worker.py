"""Background pipeline runner."""
import io
import traceback

import numpy as np
from PIL import Image

from ..database import SessionLocal
from ..models import Job, JobStatus
from ..storage import storage
from .depth import estimate_depth
from .mesh import depth_to_grid_mesh, simplify_mesh, export_glb

QUALITY_SETTINGS = {
    "fast":     {"downsample": 4, "faces": 20_000},
    "balanced": {"downsample": 2, "faces": 50_000},
    "high":     {"downsample": 1, "faces": 150_000},
}


def _set(db, job, stage, progress):
    job.stage = stage
    job.progress = progress
    db.commit()


def run_pipeline(job_id: str):
    db = SessionLocal()
    job = None
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            print(f"[Worker] Job {job_id} not found")
            return

        job.status = JobStatus.PROCESSING
        _set(db, job, "depth", 15)
        print(f"[Worker] Job {job_id} - loading image")

        img_bytes = storage.download_bytes(job.image_key)
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        max_side = 768
        w, h = image.size
        if max(w, h) > max_side:
            scale = max_side / max(w, h)
            image = image.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
            print(f"[Worker] Resized to {image.size}")

        rgb = np.array(image)

        print(f"[Worker] Estimating depth...")
        depth = estimate_depth(image)
        print(f"[Worker] Depth shape: {depth.shape}, range: {depth.min():.3f}..{depth.max():.3f}")
        _set(db, job, "mesh", 60)

        q = QUALITY_SETTINGS.get(job.quality, QUALITY_SETTINGS["balanced"])
        print(f"[Worker] Building grid mesh (downsample={q['downsample']})...")

        mesh = depth_to_grid_mesh(depth, rgb, downsample=q["downsample"])
        print(f"[Worker] Mesh: {len(mesh.vertices)} vertices, {len(mesh.faces)} faces")

        mesh = simplify_mesh(mesh, target_faces=q["faces"])
        print(f"[Worker] After simplify: {len(mesh.faces)} faces")

        _set(db, job, "export", 90)

        glb_bytes = export_glb(mesh)
        mesh_key = f"meshes/{job.id}.glb"
        storage.upload_bytes(glb_bytes, mesh_key, "model/gltf-binary")
        print(f"[Worker] Saved {len(glb_bytes)} bytes to {mesh_key}")

        job.mesh_key = mesh_key
        job.status = JobStatus.COMPLETED
        _set(db, job, "completed", 100)
        print(f"[Worker] Job {job_id} DONE")

    except Exception as e:
        traceback.print_exc()
        if job is not None:
            job.status = JobStatus.FAILED
            job.error = str(e)[:500]
            db.commit()
    finally:
        db.close()
