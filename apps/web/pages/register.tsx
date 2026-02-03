import { useState } from "react";
import Layout from "../components/Layout";

export default function Register() {
  const [form, setForm] = useState({
    email: "",
    password: "",
    name: "",
    height_cm: "",
    current_weight_kg: "",
    target_weight_kg: "",
    goal: "cut",
    activity_level: "medium",
    training_level: "beginner",
  });
  const [status, setStatus] = useState<string>("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("Отправка...");
    const payload = {
      ...form,
      height_cm: Number(form.height_cm),
      current_weight_kg: Number(form.current_weight_kg),
      target_weight_kg: Number(form.target_weight_kg),
      allergies: [],
      intolerances: [],
      dislikes: [],
      meals_per_day: 3,
      meal_time_preferences: [],
      injuries: [],
    };
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    setStatus(response.ok ? "Пользователь создан" : "Ошибка регистрации");
  };

  return (
    <Layout>
      <h1>Регистрация</h1>
      <form className="card" onSubmit={handleSubmit}>
        <label>Email</label>
        <input name="email" value={form.email} onChange={handleChange} required />
        <label>Пароль</label>
        <input name="password" type="password" value={form.password} onChange={handleChange} required />
        <label>Имя</label>
        <input name="name" value={form.name} onChange={handleChange} required />
        <label>Рост (см)</label>
        <input name="height_cm" value={form.height_cm} onChange={handleChange} required />
        <label>Текущий вес (кг)</label>
        <input name="current_weight_kg" value={form.current_weight_kg} onChange={handleChange} required />
        <label>Целевой вес (кг)</label>
        <input name="target_weight_kg" value={form.target_weight_kg} onChange={handleChange} required />
        <label>Цель</label>
        <select name="goal" value={form.goal} onChange={handleChange}>
          <option value="cut">Похудеть</option>
          <option value="bulk">Набрать массу</option>
        </select>
        <label>Активность</label>
        <select name="activity_level" value={form.activity_level} onChange={handleChange}>
          <option value="low">Низкая</option>
          <option value="medium">Средняя</option>
          <option value="high">Высокая</option>
        </select>
        <label>Уровень тренированности</label>
        <select name="training_level" value={form.training_level} onChange={handleChange}>
          <option value="beginner">Новичок</option>
          <option value="intermediate">Средний</option>
          <option value="advanced">Продвинутый</option>
        </select>
        <button type="submit">Создать</button>
      </form>
      <p>{status}</p>
    </Layout>
  );
}
