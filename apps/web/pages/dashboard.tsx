import { useEffect, useState } from "react";
import Layout from "../components/Layout";

interface PlanSummary {
  bmr: number;
  tdee: number;
  bmi_current: number;
  bmi_target: number;
  recommended_weight_range: [number, number];
  disclaimer: string;
}

export default function Dashboard() {
  const [summary, setSummary] = useState<PlanSummary | null>(null);
  const [status, setStatus] = useState("");

  const generatePlan = async () => {
    setStatus("Генерация...");
    const token = localStorage.getItem("token");
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/plans/generate`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    });
    const data = await response.json();
    setSummary(data);
    setStatus(response.ok ? "Готово" : "Ошибка");
  };

  useEffect(() => {
    setStatus("Генерируйте план для просмотра метрик.");
  }, []);

  return (
    <Layout>
      <h1>Дашборд</h1>
      <div className="card">
        <button onClick={generatePlan}>Сгенерировать планы</button>
        <p>{status}</p>
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
