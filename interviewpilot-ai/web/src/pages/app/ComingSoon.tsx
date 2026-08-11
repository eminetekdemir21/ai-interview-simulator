import type { LucideIcon } from "lucide-react"
import { Card, CardBody } from "@/components/ui"

interface ComingSoonProps {
  title: string
  description: string
  icon: LucideIcon
  phase: string
}

export function ComingSoon({ title, description, icon: Icon, phase }: ComingSoonProps) {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="font-display text-[22px] font-semibold text-ink-950 dark:text-white">{title}</h1>
        <p className="mt-1 text-[14px] text-ink-500 dark:text-ink-400">{description}</p>
      </div>
      <Card>
        <CardBody className="flex flex-col items-center justify-center gap-3 py-16 text-center">
          <div className="h-14 w-14 rounded-2xl bg-brand-50 dark:bg-brand-900/30 flex items-center justify-center">
            <Icon size={26} className="text-brand-600 dark:text-brand-300" strokeWidth={1.75} />
          </div>
          <p className="font-display text-[15px] font-semibold text-ink-900 dark:text-white">
            Bu ekran {phase} kapsamında inşa ediliyor
          </p>
          <p className="max-w-sm text-[13.5px] text-ink-500 dark:text-ink-400">
            Uygulama kabuğu ve navigasyon zaten çalışıyor — içerik faz faz gerçek verilerle doldurulacak.
          </p>
        </CardBody>
      </Card>
    </div>
  )
}
