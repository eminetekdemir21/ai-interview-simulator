import { create } from "zustand"

type Theme = "light" | "dark"

interface UIState {
  theme: Theme
  toggleTheme: () => void
  sidebarOpen: boolean
  setSidebarOpen: (open: boolean) => void
}

const getInitialTheme = (): Theme => {
  if (typeof window === "undefined") return "light"
  const stored = localStorage.getItem("ipai-theme") as Theme | null
  if (stored) return stored
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"
}

export const useUIStore = create<UIState>((set, get) => ({
  theme: getInitialTheme(),
  toggleTheme: () => {
    const next = get().theme === "dark" ? "light" : "dark"
    localStorage.setItem("ipai-theme", next)
    document.documentElement.classList.toggle("dark", next === "dark")
    set({ theme: next })
  },
  sidebarOpen: false,
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
}))
