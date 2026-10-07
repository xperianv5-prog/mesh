FROM nvidia/cuda:12.4.0-cudnn-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y \
    python3.11 python3-pip ffmpeg libgl1 libglib2.0-0 git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true
COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]