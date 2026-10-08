"""Point cloud + mesh reconstruction (grid-based, stable)."""
import numpy as np
import open3d as o3d
import trimesh


def depth_to_point_cloud(depth: np.ndarray, rgb: np.ndarray) -> o3d.geometry.PointCloud:
    """Back-project depth map to 3D points. depth normalized 0..1."""
    h, w = depth.shape
    fx = fy = max(h, w) * 1.2
    cx, cy = w / 2.0, h / 2.0

    u, v = np.meshgrid(np.arange(w), np.arange(h))
    z = depth.astype(np.float32)
    x = (u - cx) * z / fx
    y = (v - cy) * z / fy

    pts = np.stack([x, y, z], axis=-1).reshape(-1, 3)
    cols = rgb.reshape(-1, 3) / 255.0

    valid = z.reshape(-1) > 0.01
    pts = pts[valid]
    cols = cols[valid]

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pts)
    pcd.colors = o3d.utility.Vector3dVector(cols)
    return pcd


def depth_to_grid_mesh(
    depth: np.ndarray,
    rgb: np.ndarray,
    downsample: int = 2,
    depth_threshold: float = 0.02,
) -> trimesh.Trimesh:
    """
    Fast, stable mesh from depth map using grid triangulation.
    Each pixel becomes a vertex; adjacent pixels form triangles.
    """
    h, w = depth.shape

    # Downsample if needed (speed)
    if downsample > 1:
        depth = depth[::downsample, ::downsample]
        rgb = rgb[::downsample, ::downsample]
        h, w = depth.shape

    fx = fy = max(h, w) * 1.2
    cx, cy = w / 2.0, h / 2.0

    # Build 3D vertices from grid
    u, v = np.meshgrid(np.arange(w), np.arange(h))
    z = depth.astype(np.float32)
    x = (u - cx) * z / fx
    y = (v - cy) * z / fy

    vertices = np.stack([x, y, z], axis=-1).reshape(-1, 3)
    colors = rgb.reshape(-1, 3)

    # Build faces (2 triangles per grid cell)
    faces = []
    for row in range(h - 1):
        for col in range(w - 1):
            i = row * w + col
            j = i + 1
            k = i + w
            l = k + 1

            # Skip if any vertex has zero depth
            if depth[row, col] <= depth_threshold:
                continue
            if depth[row, col + 1] <= depth_threshold:
                continue
            if depth[row + 1, col] <= depth_threshold:
                continue
            if depth[row + 1, col + 1] <= depth_threshold:
                continue

            faces.append([i, j, k])
            faces.append([j, l, k])

    if not faces:
        raise RuntimeError("No faces generated (all depth values below threshold)")

    faces = np.array(faces, dtype=np.int64)

    # Remove unused vertices
    used = np.unique(faces)
    remap = -np.ones(len(vertices), dtype=np.int64)
    remap[used] = np.arange(len(used))
    vertices = vertices[used]
    colors = colors[used]
    faces = remap[faces]

    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    # Attach vertex colors
    mesh.visual.vertex_colors = np.hstack(
        [colors, np.full((len(colors), 1), 255, dtype=np.uint8)]
    )
    return mesh


def reconstruct_mesh(pcd, **kwargs) -> trimesh.Trimesh | None:
    """Placeholder — kept for API compatibility. Not used."""
    return None


def simplify_mesh(mesh: trimesh.Trimesh, target_faces: int = 50000) -> trimesh.Trimesh:
    if len(mesh.faces) <= target_faces:
        return mesh
    try:
        return mesh.simplify_quadric_decimation(target_faces)
    except Exception:
        return mesh


def export_glb(mesh: trimesh.Trimesh) -> bytes:
    return mesh.export(file_type="glb")
