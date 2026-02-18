import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { apiBaseUrl } from "../utils/api";

interface PlanSummary {
  bmr: number;
  tdee: number;
  bmi_current: number;
  bmi_target: number;
  recommended_weight_range: [number, number];
  disclaimer: string;
}

interface DashboardSummary {
  target: { calories: number; protein: number; fat: number; carbs: number };
  consumed: { calories: number; protein: number; fat: number; carbs: number };
  water_ml: number;
  rebalance: { workout_suggestion?: string };
}

export default function Dashboard() {
  const [summary, setSummary] = useState<PlanSummary | null>(null);
  const [daily, setDaily] = useState<DashboardSummary | null>(null);
  const [status, setStatus] = useState("");

  const generatePlan = async () => {
    setStatus("Генерация...");
    const token = localStorage.getItem("token");
    if (!token) {
      setStatus("Нужен вход: сначала авторизуйтесь.");
      return;
    }
    const response = await fetch(`${apiBaseUrl()}/plans/generate`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    });
    const data = await response.json();
    setSummary(data);
    setStatus(response.ok ? "Готово" : "Ошибка");
  };

  const loadSummary = async () => {
    const token = localStorage.getItem("token");
    if (!token) return;
    const day = new Date().toISOString().slice(0, 10);
    const response = await fetch(`${apiBaseUrl()}/dashboard/summary?day=${day}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (response.ok) {
      setDaily(await response.json());
    }
  };

  const addWater = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      setStatus("Нужен вход: авторизуйтесь.");
      return;
    }
    const day = new Date().toISOString().slice(0, 10);
    await fetch(`${apiBaseUrl()}/water/log`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      body: JSON.stringify({ logged_date: day, amount_ml: 250 }),
    });
    await loadSummary();
  };

  useEffect(() => {
    setStatus("Генерируйте план для просмотра метрик.");
    loadSummary();
  }, []);

  const calorieProgress =
    daily && daily.target.calories > 0
      ? Math.min(100, Math.round((daily.consumed.calories / daily.target.calories) * 100))
      : 0;

  const waterProgress = daily ? Math.min(100, Math.round((daily.water_ml / 2000) * 100)) : 0;

  return (
    <Layout>
      <h1>Дашборд</h1>
      <div className="grid two">
        <div className="widget">
          <h3>Калории сегодня</h3>
          <p>
            {daily?.consumed.calories ?? 0} / {daily?.target.calories ?? 0} ккал
          </p>
          <div className="progress">
            <span style={{ width: `${calorieProgress}%` }} />
          </div>
          {daily?.rebalance?.workout_suggestion && <p className="status">{daily.rebalance.workout_suggestion}</p>}
        </div>
        <div className="widget">
          <h3>Вода</h3>
          <div className="water-glow">
            <div>
              <p>{daily?.water_ml ?? 0} мл</p>
              <span className="pill">Цель 2000 мл</span>
            </div>
            <button onClick={addWater}>+250 мл</button>
          </div>
          <div className="progress">
            <span style={{ width: `${waterProgress}%` }} />
          </div>
        </div>
      </div>
      <div className="card">
        <button onClick={generatePlan}>Сгенерировать планы</button>
        <p className="status">{status}</p>
        {summary && (
          <div>
            <p>BMR: {summary.bmr}</p>
            <p>TDEE: {summary.tdee}</p>
            <p>ИМТ текущий: {summary.bmi_current}</p>
            <p>ИМТ целевой: {summary.bmi_target}</p>
            <p>
              Рекомендованный диапазон веса: {summary.recommended_weight_range[0]} - {" "}
              {summary.recommended_weight_range[1]} кг
            </p>
            <p>{summary.disclaimer}</p>
          </div>
        )}
      </div>
    </Layout>
  );
}
