import { useEffect, useState } from "react";
import { listJobs, getJob, Job, API_BASE } from "../api";
import { ModelViewer } from "./ModelViewer";

export function JobList({ refreshKey }: { refreshKey: number }) {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selected, setSelected] = useState<Job | null>(null);
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const data = await listJobs();
      setJobs(data);
    } catch {
      // ignore
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    const interval = setInterval(load, 3000);
    return () => clearInterval(interval);
  }, [refreshKey]);

  const selectJob = async (id: string) => {
    try {
      const data = await getJob(id);
      setSelected(data);
    } catch {}
  };

  // Build absolute mesh URL
  const meshUrl = selected?.mesh_url
    ? (selected.mesh_url.startsWith("http")
        ? selected.mesh_url
        : `${API_BASE}${selected.mesh_url}`)
    : null;

  return (
    <div className="card">
      <div className="row-between">
        <h2>My Jobs ({jobs.length})</h2>
        <button className="secondary" onClick={load} disabled={loading}>
          {loading ? "..." : "Refresh"}
        </button>
      </div>

      {jobs.length === 0 ? (
        <p style={{ color: "#94a3b8" }}>No jobs yet. Upload an image to start.</p>
      ) : (
        jobs.map((job) => (
          <div
            key={job.id}
            className="job-item"
            onClick={() => selectJob(job.id)}
            style={{ cursor: "pointer" }}
          >
            <div className="row-between" style={{ marginBottom: 4 }}>
              <span className={`badge ${job.status}`}>{job.status}</span>
              <span className="job-id">{job.id.slice(0, 8)}…</span>
            </div>
            {job.stage && (
              <div style={{ fontSize: 12, color: "#94a3b8" }}>
                {job.stage} · {job.progress ?? 0}%
              </div>
            )}
          </div>
        ))
      )}

      {selected && (
        <div style={{ marginTop: 20, padding: 16, background: "#0f172a", borderRadius: 8 }}>
          <div className="row-between" style={{ marginBottom: 12 }}>
            <h2 style={{ fontSize: 16 }}>Job Details</h2>
            <button className="secondary" onClick={() => setSelected(null)}>×</button>
          </div>

          <div style={{ display: "flex", gap: 12, flexWrap: "wrap", fontSize: 12, color: "#94a3b8", marginBottom: 12 }}>
            <span>Status: <strong style={{ color: "#f1f5f9" }}>{selected.status}</strong></span>
            {selected.stage && <span>Stage: {selected.stage}</span>}
            {selected.progress !== undefined && <span>Progress: {selected.progress}%</span>}
            {selected.quality && <span>Quality: {selected.quality}</span>}
          </div>

          {selected.error && (
            <div className="error" style={{ marginBottom: 12 }}>{selected.error}</div>
          )}

          {selected.status === "completed" && meshUrl && (
            <ModelViewer url={meshUrl} />
          )}

          {selected.status !== "completed" && selected.status !== "failed" && (
            <p style={{ color: "#94a3b8", fontSize: 13 }}>
              Processing... (refresh happens automatically every 3s)
            </p>
          )}
        </div>
      )}
    </div>
  );
}
