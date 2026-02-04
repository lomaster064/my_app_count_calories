import Link from "next/link";
import Layout from "../components/Layout";
import { apiBaseUrl } from "../utils/api";

export default function Home() {
  return (
    <Layout>
      <h1>FitFuel MVP</h1>
      <div className="card">
        <p>Платформа для похудения или набора мышечной массы.</p>
        <p>Начните с регистрации или входа.</p>
        <p className="subtitle">API по умолчанию: {apiBaseUrl()}</p>
        <Link href="/register">Регистрация</Link>
        <span> | </span>
        <Link href="/login">Вход</Link>
      </div>
    </Layout>
  );
}
