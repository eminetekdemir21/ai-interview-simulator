import { useState } from "react"
import { Search, Bell, Sun, Moon, Menu, X } from "lucide-react"
import { useUIStore } from "@/store/uiStore"
import { Avatar } from "@/components/ui"
import { useAuthStore } from "@/store/authStore"
import { MobileNav } from "./MobileNav"

export function Topbar() {
  const theme = useUIStore((s) => s.theme)
  const toggleTheme = useUIStore((s) => s.toggleTheme)
  const user = useAuthStore((s) => s.user)
  const [mobileOpen, setMobileOpen] = useState(false)

  return (
    <>
      <header className="sticky top-0 z-30 flex h-16 items-center gap-4 border-b border-ink-100 bg-white/80 backdrop-blur-md px-4 lg:px-6 dark:bg-ink-900/80 dark:border-ink-800">
        <button
          className="lg:hidden text-ink-600 dark:text-ink-300"
          onClick={() => setMobileOpen(true)}
          aria-label="Menüyü aç"
        >
          <Menu size={22} />
        </button>

        <div className="hidden sm:flex items-center flex-1 max-w-md">
          <div className="relative w-full">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-ink-400" />
            <input
              type="text"
              placeholder="Mülakat, şirket veya konu ara..."
              className="h-9 w-full rounded-lg border border-ink-200 bg-ink-50 pl-9 pr-3 text-[13.5px] text-ink-900 placeholder:text-ink-400 focus:outline-none focus:ring-2 focus:ring-brand-300 dark:bg-ink-800 dark:border-ink-700 dark:text-white"
            />
          </div>
        </div>

        <div className="ml-auto flex items-center gap-2">
          <button
            onClick={toggleTheme}
            className="h-9 w-9 flex items-center justify-center rounded-lg text-ink-500 hover:bg-ink-100 dark:text-ink-300 dark:hover:bg-ink-800 transition"
            aria-label="Temayı değiştir"
          >
            {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
          </button>
          <button
            className="relative h-9 w-9 flex items-center justify-center rounded-lg text-ink-500 hover:bg-ink-100 dark:text-ink-300 dark:hover:bg-ink-800 transition"
            aria-label="Bildirimler"
          >
            <Bell size={18} />
            <span className="absolute top-2 right-2 h-1.5 w-1.5 rounded-full bg-brand-500" />
          </button>
          {user && <Avatar name={user.name} size={34} />}
        </div>
      </header>

      {mobileOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div className="absolute inset-0 bg-black/40" onClick={() => setMobileOpen(false)} />
          <div className="absolute inset-y-0 left-0 w-72 bg-white dark:bg-ink-900 shadow-xl flex flex-col">
            <div className="flex items-center justify-between h-16 px-4 border-b border-ink-100 dark:border-ink-800">
              <span className="font-display font-semibold text-[14px]">Menü</span>
              <button onClick={() => setMobileOpen(false)} aria-label="Kapat">
                <X size={20} />
              </button>
            </div>
            <MobileNav onNavigate={() => setMobileOpen(false)} />
          </div>
        </div>
      )}
    </>
  )
}
