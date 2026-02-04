import Link from "next/link";
import React from "react";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <main>
      <div className="app-shell">
        <div className="hero">
          <div>
            <div className="brand">
              Fit<span>Fuel</span>
            </div>
            <div className="subtitle">Персональные планы питания и тренировок в одном месте.</div>
          </div>
          <nav>
            <Link href="/dashboard">Dashboard</Link>
            <Link href="/calendar">Calendar</Link>
            <Link href="/log-meal">Log meal</Link>
          </nav>
        </div>
        {children}
      </div>
    </main>
  );
}
