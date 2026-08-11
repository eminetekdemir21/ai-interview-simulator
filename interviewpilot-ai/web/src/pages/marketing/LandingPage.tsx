import { Link } from "react-router-dom"
import { Button } from "@/components/ui"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-ink-50 dark:bg-ink-950 flex flex-col items-center justify-center p-6 text-center">
      <div className="flex items-center gap-2.5 mb-8">
        <div className="h-9 w-9 rounded-lg grad-bg flex items-center justify-center">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
            <path d="M4 12L10 18L20 6" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </div>
        <span className="font-display font-semibold text-[17px]">InterviewPilot <span className="text-brand-600">AI</span></span>
      </div>
      <h1 className="font-display text-[36px] sm:text-[46px] font-semibold tracking-tight max-w-2xl">
        Practice smarter. <span className="grad-text">Interview better.</span>
      </h1>
      <p className="mt-4 max-w-lg text-[15px] text-ink-500 dark:text-ink-400">
        Landing page içeriği Faz 3'te tamamlanacak. Uygulamayı denemek için giriş yap.
      </p>
      <div className="mt-8 flex gap-3">
        <Link to="/login"><Button size="lg">Ücretsiz Mülakata Başla</Button></Link>
        <Link to="/app/dashboard"><Button size="lg" variant="outline">Dashboard'u gör</Button></Link>
      </div>
    </div>
  )
}
