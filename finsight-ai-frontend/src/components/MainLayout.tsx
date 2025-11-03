'use client';

import { Sidebar } from './Sidebar';
import { Navbar } from './Navbar';

export function MainLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <div className="pl-64">
        <Navbar />
        <main className="min-h-[calc(100vh-4rem)] pt-16">
          {children}
        </main>
      </div>
    </div>
  );
}
