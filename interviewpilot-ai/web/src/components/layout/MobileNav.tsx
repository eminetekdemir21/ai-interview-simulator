import { NavLink } from "react-router-dom"
import { cn } from "@/lib/utils"
import {
  LayoutDashboard, FileText, Target, Building2, MessageSquare, Code2,
  History, BarChart3, Map, Trophy, Sparkles, User, Settings, LogOut,
} from "lucide-react"
import { useAuthStore } from "@/store/authStore"

const nav = [
  { to: "/app/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/app/resume-analysis", label: "Resume Analysis", icon: FileText },
  { to: "/app/job-match", label: "Job Match", icon: Target },
  { to: "/app/companies", label: "Company Interviews", icon: Building2 },
  { to: "/app/interview-practice", label: "Interview Practice", icon: MessageSquare },
  { to: "/app/live-coding", label: "Live Coding", icon: Code2 },
  { to: "/app/history", label: "Interview History", icon: History },
  { to: "/app/analytics", label: "Analytics", icon: BarChart3 },
  { to: "/app/roadmap", label: "Learning Roadmap", icon: Map },
  { to: "/app/achievements", label: "Achievements", icon: Trophy },
  { to: "/app/career-coach", label: "AI Career Coach", icon: Sparkles },
  { to: "/app/profile", label: "Profile", icon: User },
  { to: "/app/settings", label: "Settings", icon: Settings },
]

export function MobileNav({ onNavigate }: { onNavigate: () => void }) {
  const logout = useAuthStore((s) => s.logout)
  return (
    <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-0.5">
      {nav.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          onClick={onNavigate}
          className={({ isActive }) =>
            cn(
              "flex items-center gap-3 rounded-lg px-3 py-2.5 text-[13.5px] font-medium transition",
              isActive
                ? "bg-brand-50 text-brand-700 dark:bg-brand-900/30 dark:text-brand-300"
                : "text-ink-600 hover:bg-ink-50 dark:text-ink-400 dark:hover:bg-ink-800"
            )
          }
        >
          <item.icon size={17} />
          {item.label}
        </NavLink>
      ))}
      <button
        onClick={() => { logout(); onNavigate() }}
        className="w-full flex items-center gap-3 rounded-lg px-3 py-2.5 text-[13.5px] font-medium text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 transition"
      >
        <LogOut size={17} />
        Logout
      </button>
    </nav>
  )
}
