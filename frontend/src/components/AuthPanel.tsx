import { useState } from "react";
import { register, login } from "../api";

export function AuthPanel({ onSuccess }: { onSuccess: () => void }) {
  const [mode, setMode] = useState<"login" | "register">("register");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      if (mode === "register") {
        await register(email, password);
      } else {
        await login(email, password);
      }
      onSuccess();
    } catch (err: any) {
      setError(err.message || "Something went wrong");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="card" style={{ maxWidth: 420, margin: "80px auto" }}>
      <h1 style={{ marginBottom: 8 }}>mesh</h1>
      <p className="subtitle" style={{ marginBottom: 20 }}>
        2D → 3D mesh generator
      </p>

      <div className="tabs">
        <button
          className={mode === "register" ? "active" : ""}
          onClick={() => { setMode("register"); setError(null); }}
          type="button"
        >
          Register
        </button>
        <button
          className={mode === "login" ? "active" : ""}
          onClick={() => { setMode("login"); setError(null); }}
          type="button"
        >
          Login
        </button>
      </div>

      <form onSubmit={submit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password (min 6 chars)"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={6}
        />

        {error && <div className="error">{error}</div>}

        <button type="submit" disabled={busy} style={{ width: "100%" }}>
          {busy ? "..." : mode === "register" ? "Create account" : "Log in"}
        </button>
      </form>
    </div>
  );
}
