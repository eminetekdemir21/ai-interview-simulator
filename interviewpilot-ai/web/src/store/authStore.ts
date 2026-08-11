import { create } from "zustand"

export interface MockUser {
  id: string
  name: string
  email: string
  targetRole: string
  onboarded: boolean
}

interface AuthState {
  user: MockUser | null
  isAuthenticated: boolean
  login: (email: string) => void
  logout: () => void
  completeOnboarding: (targetRole: string) => void
}

const DEMO_USER: MockUser = {
  id: "u_demo",
  name: "Alex Morgan",
  email: "alex.morgan@example.com",
  targetRole: "Senior Backend Developer",
  onboarded: true,
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  login: (_email: string) => set({ user: DEMO_USER, isAuthenticated: true }),
  logout: () => set({ user: null, isAuthenticated: false }),
  completeOnboarding: (targetRole: string) =>
    set((s) => (s.user ? { user: { ...s.user, targetRole, onboarded: true } } : s)),
}))
