import { AreaChart, Area, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts"
import { Card, CardBody, Badge, ScoreRing } from "@/components/ui"
import { Sparkles, TrendingUp, Flame, Clock, MessageSquare } from "lucide-react"
import { demoUser, weeklyPerformance, recentInterviews, aiRecommendation } from "@/data/mockData"
import { useAuthStore } from "@/store/authStore"

const kpis = [
  { label: "Genel Skor", value: demoUser.overallScore, suffix: "", icon: TrendingUp, tone: "brand" as const },
  { label: "Toplam Mülakat", value: demoUser.totalInterviews, suffix: "", icon: MessageSquare, tone: "info" as const },
  { label: "Seri", value: demoUser.streak, suffix: " gün", icon: Flame, tone: "warning" as const },
  { label: "Pratik Süresi", value: demoUser.practiceHours, suffix: " sa", icon: Clock, tone: "neutral" as const },
]

function greeting() {
  const h = new Date().getHours()
  if (h < 6) return "İyi geceler"
  if (h < 12) return "Günaydın"
  if (h < 18) return "İyi günler"
  return "İyi akşamlar"
}

export default function DashboardPage() {
  const user = useAuthStore((s) => s.user)
  const firstName = user?.name?.split(" ")[0] ?? demoUser.name.split(" ")[0]

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="font-display text-[22px] font-semibold text-ink-950 dark:text-white">
          {greeting()}, {firstName}
        </h1>
        <p className="mt-1 text-[14px] text-ink-500 dark:text-ink-400">İşte mülakat hazırlık durumun.</p>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {kpis.map((kpi) => (
          <Card key={kpi.label}>
            <CardBody className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-xl bg-ink-50 dark:bg-ink-800 flex items-center justify-center shrink-0">
                <kpi.icon size={18} className="text-brand-600 dark:text-brand-300" />
              </div>
              <div>
                <p className="text-[12px] text-ink-500 dark:text-ink-400">{kpi.label}</p>
                <p className="font-display text-[20px] font-semibold text-ink-950 dark:text-white">
                  {kpi.value}
                  <span className="text-[13px] font-medium text-ink-400">{kpi.suffix}</span>
                </p>
              </div>
            </CardBody>
          </Card>
        ))}
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardBody>
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="font-display text-[15px] font-semibold text-ink-950 dark:text-white">Haftalık Performans</h3>
                <p className="text-[12.5px] text-ink-500 dark:text-ink-400">Son 7 günlük ortalama mülakat skorların</p>
              </div>
              <Badge tone="success">+16 bu hafta</Badge>
            </div>
            <div className="h-56">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={weeklyPerformance} margin={{ top: 5, right: 5, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="scoreFill" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#6d4dff" stopOpacity={0.3} />
                      <stop offset="100%" stopColor="#6d4dff" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="day" tick={{ fontSize: 12, fill: "#8a8aa3" }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fontSize: 12, fill: "#8a8aa3" }} axisLine={false} tickLine={false} domain={[50, 100]} />
                  <Tooltip contentStyle={{ borderRadius: 12, border: "1px solid #eeeef4", fontSize: 13 }} />
                  <Area type="monotone" dataKey="score" stroke="#6d4dff" strokeWidth={2.5} fill="url(#scoreFill)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody className="flex flex-col items-center text-center gap-3">
            <p className="text-[13px] font-medium text-ink-500 dark:text-ink-400">Mülakat Hazırlık Skoru</p>
            <ScoreRing value={demoUser.overallScore} size={112} />
            <div className="w-full grid grid-cols-2 gap-2 mt-2 text-left">
              <div className="rounded-lg bg-ink-50 dark:bg-ink-800 p-2.5">
                <p className="text-[11px] text-ink-500 dark:text-ink-400">Güçlü</p>
                <p className="text-[13px] font-semibold text-ink-950 dark:text-white">{demoUser.strongestSkill}</p>
              </div>
              <div className="rounded-lg bg-ink-50 dark:bg-ink-800 p-2.5">
                <p className="text-[11px] text-ink-500 dark:text-ink-400">Zayıf</p>
                <p className="text-[13px] font-semibold text-ink-950 dark:text-white">{demoUser.weakestSkill}</p>
              </div>
            </div>
          </CardBody>
        </Card>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardBody>
            <h3 className="font-display text-[15px] font-semibold text-ink-950 dark:text-white mb-4">Son Mülakatlar</h3>
            <div className="space-y-1">
              {recentInterviews.map((iv) => (
                <div
                  key={iv.id}
                  className="flex items-center gap-3 rounded-xl px-3 py-2.5 hover:bg-ink-50 dark:hover:bg-ink-800 transition"
                >
                  <div className="h-9 w-9 rounded-lg bg-ink-50 dark:bg-ink-800 flex items-center justify-center text-[11px] font-semibold text-ink-600 dark:text-ink-300 shrink-0">
                    {iv.company.slice(0, 2).toUpperCase()}
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="text-[13.5px] font-medium text-ink-950 dark:text-white truncate">
                      {iv.company} · {iv.role}
                    </p>
                    <p className="text-[12px] text-ink-500 dark:text-ink-400">
                      {iv.type} · {iv.difficulty} · {iv.date}
                    </p>
                  </div>
                  <span
                    className={`font-display text-[15px] font-semibold ${
                      iv.score >= 85 ? "text-emerald-600" : iv.score >= 70 ? "text-brand-600" : "text-amber-600"
                    }`}
                  >
                    {iv.score}
                  </span>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>

        <Card className="bg-gradient-to-br from-brand-600 via-brand-600 to-blue-600 border-none">
          <CardBody className="text-white">
            <div className="flex items-center gap-2 mb-3">
              <Sparkles size={16} />
              <span className="text-[12.5px] font-semibold uppercase tracking-wide text-brand-100">AI Önerisi</span>
            </div>
            <p className="text-[14px] leading-relaxed">{aiRecommendation}</p>
          </CardBody>
        </Card>
      </div>
    </div>
  )
}
