import { useState } from "react";
import { uploadImage } from "../api";

export function UploadPanel({ onUploaded }: { onUploaded: () => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [prompt, setPrompt] = useState("object");
  const [quality, setQuality] = useState("fast");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleFile = (f: File | null) => {
    setFile(f);
    setError(null);
    setSuccess(null);
    if (f) setPreview(URL.createObjectURL(f));
    else setPreview(null);
  };

  const submit = async () => {
    if (!file) return;
    setBusy(true);
    setError(null);
    setSuccess(null);
    try {
      const res = await uploadImage(file, prompt, quality);
      setSuccess(`Uploaded! Job ID: ${res.job_id}`);
      setFile(null);
      setPreview(null);
      onUploaded();
    } catch (err: any) {
      setError(err.message || "Upload failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="card">
      <h2>Upload Image</h2>

      <label className="file-input">
        {file ? `📎 ${file.name}` : "📁 Click to select an image"}
        <input
          type="file"
          accept="image/*"
          style={{ display: "none" }}
          onChange={(e) => handleFile(e.target.files?.[0] || null)}
        />
      </label>

      {preview && (
        <img src={preview} alt="preview" className="image-preview" />
      )}

      <div style={{ marginTop: 16 }}>
        <input
          type="text"
          placeholder="Prompt (e.g. object, chair, table)"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />

        <div className="row" style={{ marginTop: 8 }}>
          <label>Quality:</label>
          {["fast", "balanced", "high"].map((q) => (
            <button
              key={q}
              type="button"
              className={quality === q ? "" : "secondary"}
              onClick={() => setQuality(q)}
              style={{ padding: "6px 14px" }}
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      {error && <div className="error" style={{ marginTop: 12 }}>{error}</div>}
      {success && <div className="success" style={{ marginTop: 12 }}>{success}</div>}

      <button
        onClick={submit}
        disabled={!file || busy}
        style={{ width: "100%", marginTop: 16 }}
      >
        {busy ? "Uploading..." : "Upload & Create Job"}
      </button>
    </div>
  );
}
