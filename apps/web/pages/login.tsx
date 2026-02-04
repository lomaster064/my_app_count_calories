import { useState } from "react";
import Layout from "../components/Layout";
import { apiBaseUrl } from "../utils/api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const response = await fetch(`${apiBaseUrl()}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    if (response.ok) {
      localStorage.setItem("token", data.access_token);
      setStatus("Успешный вход");
      setError("");
    } else {
      setStatus("");
      setError(data.detail || "Ошибка входа");
    }
  };

  return (
    <Layout>
      <h1>Вход</h1>
      <form className="card" onSubmit={handleSubmit}>
        <label>Email</label>
        <input value={email} onChange={(e) => setEmail(e.target.value)} />
        <label>Пароль</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button type="submit">Войти</button>
      </form>
      {status && <p className="status">{status}</p>}
      {error && <p className="error">{error}</p>}
    </Layout>
  );
}
