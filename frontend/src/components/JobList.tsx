import { useEffect, useState } from "react";
import { listJobs, getJob, Job } from "../api";

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
    const interval = setInterval(load, 5000);
    return () => clearInterval(interval);
  }, [refreshKey]);

  const selectJob = async (id: string) => {
    try {
      const data = await getJob(id);
      setSelected(data);
    } catch {}
  };

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
            {job.created_at && (
              <div style={{ fontSize: 12, color: "#94a3b8" }}>{job.created_at}</div>
            )}
          </div>
        ))
      )}

      {selected && (
        <div style={{ marginTop: 20, padding: 16, background: "#0f172a", borderRadius: 8 }}>
          <div className="row-between">
            <h2 style={{ fontSize: 16 }}>Job Details</h2>
            <button className="secondary" onClick={() => setSelected(null)}>×</button>
          </div>
          <pre style={{ fontSize: 12, color: "#cbd5e1", overflow: "auto" }}>
            {JSON.stringify(selected, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
