import { useState } from "react";
import Layout from "../components/Layout";

export default function LogMeal() {
  const [text, setText] = useState("");
  const [status, setStatus] = useState("");
  const [file, setFile] = useState<File | null>(null);

  const submitText = async () => {
    setStatus("Отправка...");
    const token = localStorage.getItem("token");
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/meal-logs`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({
        logged_date: new Date().toISOString().slice(0, 10),
        notes: text,
        items: [],
      }),
    });
    setStatus(response.ok ? "Сохранено" : "Ошибка");
  };

  const submitPhoto = async () => {
    if (!file) return;
    setStatus("Загрузка фото...");
    const token = localStorage.getItem("token");
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/meal-logs/photo?logged_date=${new Date().toISOString().slice(0, 10)}`,
      {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      }
    );
    const data = await response.json();
    setStatus(response.ok ? JSON.stringify(data.result) : "Ошибка");
  };

  return (
    <Layout>
      <h1>Логирование приема пищи</h1>
      <div className="card">
        <label>Описание приема пищи</label>
        <textarea value={text} onChange={(e) => setText(e.target.value)} />
        <button onClick={submitText}>Отправить текст</button>
      </div>
      <div className="card">
        <label>Загрузить фото</label>
        <input type="file" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
        <button onClick={submitPhoto}>Отправить фото</button>
      </div>
      <p>{status}</p>
    </Layout>
  );
}
