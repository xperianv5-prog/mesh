import os
from .config import settings


class LocalStorage:
    def __init__(self):
        self.root = settings.LOCAL_STORAGE_ROOT
        os.makedirs(self.root, exist_ok=True)

    def _path(self, key):
        p = os.path.join(self.root, key)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        return p

    def upload_bytes(self, data, key, content_type=None):
        with open(self._path(key), "wb") as f:
            f.write(data)
        return key

    def presigned_url(self, key, expires=3600):
        return f"/files/{key}"

    def download_bytes(self, key):
        with open(os.path.join(self.root, key), "rb") as f:
            return f.read()


storage = LocalStorage()
