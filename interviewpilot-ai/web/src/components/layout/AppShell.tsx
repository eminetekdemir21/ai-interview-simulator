import { Outlet, Navigate } from "react-router-dom"
import { Sidebar } from "./Sidebar"
import { Topbar } from "./Topbar"
import { useAuthStore } from "@/store/authStore"

export function AppShell() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated)

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return (
    <div className="min-h-screen bg-ink-50 dark:bg-ink-950">
      <Sidebar />
      <div className="lg:pl-64">
        <Topbar />
        <main className="p-4 sm:p-6 lg:p-8 max-w-[1400px] mx-auto">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
