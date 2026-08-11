import { useState, type FormEvent } from "react"
import { useNavigate, Link } from "react-router-dom"
import { Button, Input, Label } from "@/components/ui"
import { useAuthStore } from "@/store/authStore"

export default function LoginPage() {
  const navigate = useNavigate()
  const login = useAuthStore((s) => s.login)
  const [email, setEmail] = useState("alex.morgan@example.com")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (!email || !password) {
      setError("E-posta ve şifre gerekli.")
      return
    }
    login(email)
    navigate("/app/dashboard")
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-ink-50 dark:bg-ink-950 p-6">
      <div className="w-full max-w-sm">
        <div className="flex items-center gap-2.5 justify-center mb-8">
          <div className="h-8 w-8 rounded-lg grad-bg flex items-center justify-center">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <path d="M4 12L10 18L20 6" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>
          <span className="font-display font-semibold text-[15px]">InterviewPilot <span className="text-brand-600">AI</span></span>
        </div>

        <div className="rounded-2xl border border-ink-100 dark:border-ink-800 bg-white dark:bg-ink-900 shadow-soft p-6">
          <h1 className="font-display text-[19px] font-semibold text-ink-950 dark:text-white">Tekrar hoş geldin</h1>
          <p className="mt-1 text-[13.5px] text-ink-500 dark:text-ink-400">Devam etmek için giriş yap.</p>

          <form onSubmit={handleSubmit} className="mt-6 space-y-4">
            <div>
              <Label htmlFor="email">E-posta</Label>
              <Input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="ornek@sirket.com" />
            </div>
            <div>
              <Label htmlFor="password">Şifre</Label>
              <Input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" error={error} />
            </div>
            <div className="flex items-center justify-end">
              <Link to="/forgot-password" className="text-[12.5px] font-medium text-brand-600 hover:text-brand-700">Şifreni mi unuttun?</Link>
            </div>
            <Button type="submit" className="w-full">Giriş yap</Button>
          </form>

          <p className="mt-5 text-center text-[13px] text-ink-500 dark:text-ink-400">
            Hesabın yok mu? <Link to="/register" className="font-medium text-brand-600 hover:text-brand-700">Kayıt ol</Link>
          </p>
        </div>

        <p className="mt-4 text-center text-[12px] text-ink-400">
          Demo modu: herhangi bir e-posta/şifre ile giriş yapabilirsin.
        </p>
      </div>
    </div>
  )
}
