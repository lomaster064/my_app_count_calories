import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { apiBaseUrl } from "../utils/api";

interface DayItem {
  id: number;
  date: string;
  total_calories: number;
}

export default function Calendar() {
  const [days, setDays] = useState<DayItem[]>([]);

  useEffect(() => {
    const fetchPlan = async () => {
      const token = localStorage.getItem("token");
      const response = await fetch(`${apiBaseUrl()}/plans`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.ok) {
        const data = await response.json();
        setDays(data.days || []);
      }
    };
    fetchPlan();
  }, []);

  return (
    <Layout>
      <h1>Календарь питания</h1>
      <div className="card">
        {days.map((day) => (
          <div key={day.id}>
            {day.date}: {day.total_calories} ккал
          </div>
        ))}
      </div>
    </Layout>
  );
}
