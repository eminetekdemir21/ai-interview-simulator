import { type HTMLAttributes } from "react"
import { cn } from "@/lib/utils"

type Tone = "brand" | "success" | "warning" | "danger" | "neutral" | "info"

const toneClasses: Record<Tone, string> = {
  brand: "bg-brand-50 text-brand-700 border-brand-100 dark:bg-brand-900/30 dark:text-brand-300 dark:border-brand-800",
  success: "bg-emerald-50 text-emerald-700 border-emerald-100 dark:bg-emerald-900/30 dark:text-emerald-300 dark:border-emerald-800",
  warning: "bg-amber-50 text-amber-700 border-amber-100 dark:bg-amber-900/30 dark:text-amber-300 dark:border-amber-800",
  danger: "bg-red-50 text-red-700 border-red-100 dark:bg-red-900/30 dark:text-red-300 dark:border-red-800",
  neutral: "bg-ink-100 text-ink-600 border-ink-200 dark:bg-ink-800 dark:text-ink-300 dark:border-ink-700",
  info: "bg-blue-50 text-blue-700 border-blue-100 dark:bg-blue-900/30 dark:text-blue-300 dark:border-blue-800",
}

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  tone?: Tone
}

export function Badge({ className, tone = "neutral", ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full border px-2.5 py-1 text-[12px] font-medium",
        toneClasses[tone],
        className
      )}
      {...props}
    />
  )
}
