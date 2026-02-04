import { useState } from "react";
import Layout from "../components/Layout";

export default function Onboarding() {
  const [form, setForm] = useState({
    diet_type: "",
    allergies: "",
    intolerances: "",
    dislikes: "",
    injuries: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  return (
    <Layout>
      <h1>Анкета пользователя</h1>
      <div className="card">
        <label>Тип питания (веган/вегетарианец/религия)</label>
        <input name="diet_type" value={form.diet_type} onChange={handleChange} />
        <label>Аллергии (через запятую)</label>
        <input name="allergies" value={form.allergies} onChange={handleChange} />
        <label>Непереносимости</label>
        <input name="intolerances" value={form.intolerances} onChange={handleChange} />
        <label>Не люблю</label>
        <input name="dislikes" value={form.dislikes} onChange={handleChange} />
        <label>Травмы и ограничения</label>
        <textarea name="injuries" value={form.injuries} onChange={handleChange} />
        <p className="status">Данные анкеты сохраняются через API профиля.</p>
      </div>
    </Layout>
  );
}
