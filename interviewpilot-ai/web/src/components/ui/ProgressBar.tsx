import { cn } from "@/lib/utils"

interface ProgressBarProps {
  value: number
  className?: string
  tone?: "brand" | "success" | "warning" | "danger"
}

const toneClasses = {
  brand: "grad-bg",
  success: "bg-emerald-500",
  warning: "bg-amber-500",
  danger: "bg-red-500",
}

export function ProgressBar({ value, className, tone = "brand" }: ProgressBarProps) {
  const clamped = Math.max(0, Math.min(100, value))
  return (
    <div className={cn("h-2 w-full overflow-hidden rounded-full bg-ink-100 dark:bg-ink-800", className)}>
      <div
        className={cn("h-full rounded-full transition-all duration-500", toneClasses[tone])}
        style={{ width: `${clamped}%` }}
      />
    </div>
  )
}
