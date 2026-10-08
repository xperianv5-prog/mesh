import { useState, useEffect } from "react";
import { AuthPanel } from "./components/AuthPanel";
import { UploadPanel } from "./components/UploadPanel";
import { JobList } from "./components/JobList";
import { getToken, logout, API_BASE } from "./api";

export default function App() {
  const [authed, setAuthed] = useState<boolean>(!!getToken());
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    setAuthed(!!getToken());
  }, []);

  if (!authed) {
    return (
      <div className="container">
        <AuthPanel onSuccess={() => setAuthed(true)} />
      </div>
    );
  }

  return (
    <div className="container">
      <div className="header">
        <div>
          <h1>mesh</h1>
          <p className="subtitle" style={{ marginBottom: 0 }}>
            2D → 3D mesh generator
          </p>
        </div>
        <div className="row">
          <span className="user-email">{API_BASE}</span>
          <button
            className="secondary"
            onClick={() => { logout(); setAuthed(false); }}
          >
            Logout
          </button>
        </div>
      </div>

      <UploadPanel onUploaded={() => setRefreshKey((k) => k + 1)} />
      <JobList refreshKey={refreshKey} />
    </div>
  );
}
