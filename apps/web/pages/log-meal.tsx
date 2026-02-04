import { useState } from "react";
import Layout from "../components/Layout";
import { apiBaseUrl } from "../utils/api";

export default function LogMeal() {
  const [text, setText] = useState("");
  const [calories, setCalories] = useState("0");
  const [protein, setProtein] = useState("0");
  const [fat, setFat] = useState("0");
  const [carbs, setCarbs] = useState("0");
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");
  const [file, setFile] = useState<File | null>(null);

  const submitText = async () => {
    setStatus("Отправка...");
    setError("");
    const token = localStorage.getItem("token");
    if (!token) {
      setStatus("");
      setError("Нужен вход: авторизуйтесь перед логированием.");
      return;
    }
    const response = await fetch(`${apiBaseUrl()}/meal-logs`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({
        logged_date: new Date().toISOString().slice(0, 10),
        notes: text,
        items: [
          {
            name: text || "Ручной ввод",
            grams_estimate: 0,
            calories: Number(calories),
            protein: Number(protein),
            fat: Number(fat),
            carbs: Number(carbs),
            confidence: 1,
          },
        ],
      }),
    });
    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      setError(data.detail || "Ошибка сохранения");
      setStatus("");
      return;
    }
    setStatus("Сохранено");
  };

  const submitPhoto = async () => {
    if (!file) return;
    setStatus("Загрузка фото...");
    setError("");
    const token = localStorage.getItem("token");
    if (!token) {
      setStatus("");
      setError("Нужен вход: авторизуйтесь перед загрузкой фото.");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch(
      `${apiBaseUrl()}/meal-logs/photo?logged_date=${new Date().toISOString().slice(0, 10)}`,
      {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      }
    );
    const data = await response.json();
    if (!response.ok) {
      setError(data.detail || "Ошибка");
      setStatus("");
      return;
    }
    setStatus(JSON.stringify(data.result));
  };

  return (
    <Layout>
      <h1>Логирование приема пищи</h1>
      <div className="card">
        <label>Описание приема пищи</label>
        <textarea value={text} onChange={(e) => setText(e.target.value)} />
        <label>Калории (ккал)</label>
        <input value={calories} onChange={(e) => setCalories(e.target.value)} />
        <div className="grid two">
          <div>
            <label>Белки (г)</label>
            <input value={protein} onChange={(e) => setProtein(e.target.value)} />
          </div>
          <div>
            <label>Жиры (г)</label>
            <input value={fat} onChange={(e) => setFat(e.target.value)} />
          </div>
        </div>
        <label>Углеводы (г)</label>
        <input value={carbs} onChange={(e) => setCarbs(e.target.value)} />
        <button onClick={submitText}>Отправить текст</button>
      </div>
      <div className="card">
        <label>Загрузить фото</label>
        <input type="file" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
        <button onClick={submitPhoto} className="secondary">
          Отправить фото
        </button>
      </div>
      {status && <p className="status">{status}</p>}
      {error && <p className="error">{error}</p>}
    </Layout>
  );
}
