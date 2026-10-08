"""Depth estimation with Depth Anything V2."""
import numpy as np
import torch
from PIL import Image
from transformers import pipeline

DEVICE = 0 if torch.cuda.is_available() else -1

_pipe = None


def _get_pipe():
    global _pipe
    if _pipe is None:
        print("[Depth] Loading Depth-Anything-V2-Small...")
        _pipe = pipeline(
            task="depth-estimation",
            model="depth-anything/Depth-Anything-V2-Small-hf",
            device=DEVICE,
        )
        print(f"[Depth] Loaded on device {DEVICE}")
    return _pipe


def estimate_depth(image: Image.Image) -> np.ndarray:
    """Returns float32 depth map (H, W), normalized 0..1. Larger = closer."""
    pipe = _get_pipe()
    result = pipe(image)
    depth = result["depth"]
    depth = np.array(depth, dtype=np.float32)
    dmin, dmax = float(depth.min()), float(depth.max())
    if dmax - dmin < 1e-6:
        return np.zeros_like(depth)
    return (depth - dmin) / (dmax - dmin)
