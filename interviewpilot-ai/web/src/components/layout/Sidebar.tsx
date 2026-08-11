import { NavLink } from "react-router-dom"
import { cn } from "@/lib/utils"
import {
  LayoutDashboard,
  FileText,
  Target,
  Building2,
  MessageSquare,
  Code2,
  History,
  BarChart3,
  Map,
  Trophy,
  Sparkles,
  User,
  Settings,
  LogOut,
} from "lucide-react"
import { useAuthStore } from "@/store/authStore"
import { Avatar } from "@/components/ui"

const mainNav = [
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
]

const bottomNav = [
  { to: "/app/career-coach", label: "AI Career Coach", icon: Sparkles },
  { to: "/app/profile", label: "Profile", icon: User },
  { to: "/app/settings", label: "Settings", icon: Settings },
]

export function Sidebar() {
  const user = useAuthStore((s) => s.user)
  const logout = useAuthStore((s) => s.logout)

  return (
    <aside className="hidden lg:flex lg:w-64 lg:flex-col lg:fixed lg:inset-y-0 border-r border-ink-100 bg-white dark:bg-ink-900 dark:border-ink-800">
      <div className="flex items-center gap-2.5 px-5 h-16 border-b border-ink-100 dark:border-ink-800 shrink-0">
        <div className="h-8 w-8 rounded-lg grad-bg flex items-center justify-center shadow-soft shrink-0">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M4 12L10 18L20 6" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </div>
        <span className="font-display font-semibold text-[14.5px] tracking-tight text-ink-950 dark:text-white">
          InterviewPilot <span className="text-brand-600">AI</span>
        </span>
      </div>

      <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-0.5">
        {mainNav.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 rounded-lg px-3 py-2.5 text-[13.5px] font-medium transition",
                isActive
                  ? "bg-brand-50 text-brand-700 dark:bg-brand-900/30 dark:text-brand-300"
                  : "text-ink-600 hover:bg-ink-50 hover:text-ink-950 dark:text-ink-400 dark:hover:bg-ink-800 dark:hover:text-white"
              )
            }
          >
            <item.icon size={17} strokeWidth={2} className="shrink-0" />
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="px-3 py-4 border-t border-ink-100 dark:border-ink-800 space-y-0.5">
        {bottomNav.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 rounded-lg px-3 py-2.5 text-[13.5px] font-medium transition",
                isActive
                  ? "bg-brand-50 text-brand-700 dark:bg-brand-900/30 dark:text-brand-300"
                  : "text-ink-600 hover:bg-ink-50 hover:text-ink-950 dark:text-ink-400 dark:hover:bg-ink-800 dark:hover:text-white"
              )
            }
          >
            <item.icon size={17} strokeWidth={2} className="shrink-0" />
            {item.label}
          </NavLink>
        ))}
        <button
          onClick={logout}
          className="w-full flex items-center gap-3 rounded-lg px-3 py-2.5 text-[13.5px] font-medium text-ink-600 hover:bg-red-50 hover:text-red-600 dark:text-ink-400 dark:hover:bg-red-900/20 dark:hover:text-red-400 transition"
        >
          <LogOut size={17} strokeWidth={2} />
          Logout
        </button>

        {user && (
          <div className="mt-3 flex items-center gap-2.5 rounded-lg px-2.5 py-2 bg-ink-50 dark:bg-ink-800">
            <Avatar name={user.name} size={32} />
            <div className="min-w-0">
              <p className="truncate text-[13px] font-semibold text-ink-950 dark:text-white">{user.name}</p>
              <p className="truncate text-[11.5px] text-ink-500 dark:text-ink-400">{user.targetRole}</p>
            </div>
          </div>
        )}
      </div>
    </aside>
  )
}
