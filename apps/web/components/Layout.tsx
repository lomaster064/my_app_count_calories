import Link from "next/link";
import React from "react";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <main>
      <nav>
        <Link href="/dashboard">Dashboard</Link>
        <Link href="/calendar">Calendar</Link>
        <Link href="/log-meal">Log meal</Link>
      </nav>
      {children}
    </main>
  );
}
