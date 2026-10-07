# mesh

2D -> 3D mesh generator with semantic segmentation, depth estimation, and
per-object reconstruction.

## Pipeline

1. Semantic segmentation (SAM 2)
2. Depth estimation (Depth Anything V2)
3. Relationship analysis (scene graph)
4. Mesh reconstruction (Poisson per object)
5. Optimization (decimation)

## Quick start

cp backend/.env.example backend/.env
docker compose up --build


## License

MIT