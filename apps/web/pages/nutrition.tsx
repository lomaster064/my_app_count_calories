import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { apiBaseUrl } from "../utils/api";

interface DayPlan {
  id: number;
  date: string;
  total_calories: number;
  meals: { id: number; name: string; items: { recipe_id: number }[] }[];
}

interface Recipe {
  id: number;
  name: string;
}

export default function Nutrition() {
  const [days, setDays] = useState<DayPlan[]>([]);
  const [recipes, setRecipes] = useState<Record<number, string>>({});
  const [status, setStatus] = useState("");
  const [range, setRange] = useState(3);

  const loadRecipes = async () => {
    const response = await fetch(`${apiBaseUrl()}/recipes`);
    if (!response.ok) return;
    const data: Recipe[] = await response.json();
    const map: Record<number, string> = {};
    data.forEach((recipe) => {
      map[recipe.id] = recipe.name;
    });
    setRecipes(map);
  };

  const generatePlan = async (daysCount: number) => {
    setStatus("Генерация плана...");
    const token = localStorage.getItem("token");
    if (!token) {
      setStatus("Нужен вход: авторизуйтесь.");
      return;
    }
    const response = await fetch(`${apiBaseUrl()}/plans/generate?days=${daysCount}`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    });
    const data = await response.json();
    if (!response.ok) {
      setStatus(data.detail || "Ошибка генерации");
      return;
    }
    setDays(data.plan.days || []);
    setStatus("Готово");
  };

  useEffect(() => {
    loadRecipes();
    generatePlan(range);
  }, [range]);

  return (
    <Layout>
      <h1>Питание</h1>
      <div className="card">
        <p>Выберите период:</p>
        <div className="grid two">
          {[1, 3, 5, 7].map((value) => (
            <button key={value} onClick={() => setRange(value)} className={range === value ? "" : "secondary"}>
              {value} день
            </button>
          ))}
        </div>
        <p className="status">{status}</p>
      </div>
      <div className="grid">
        {days.map((day) => (
          <div key={day.id} className="card">
            <h3>{day.date}</h3>
            <p>Калории: {day.total_calories}</p>
            {day.meals.map((meal) => (
              <div key={meal.id} className="widget">
                <strong>{meal.name}</strong>
                <ul>
                  {meal.items.map((item) => (
                    <li key={`${meal.id}-${item.recipe_id}`}>{recipes[item.recipe_id] || `Рецепт #${item.recipe_id}`}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        ))}
      </div>
    </Layout>
  );
}
