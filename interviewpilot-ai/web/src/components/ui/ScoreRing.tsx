import { cn } from "@/lib/utils"

interface ScoreRingProps {
  value: number
  size?: number
  strokeWidth?: number
  className?: string
  label?: string
}

export function ScoreRing({ value, size = 96, strokeWidth = 8, className, label }: ScoreRingProps) {
  const clamped = Math.max(0, Math.min(100, value))
  const radius = (size - strokeWidth) / 2
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (clamped / 100) * circumference

  const color =
    clamped >= 80 ? "#10b981" : clamped >= 60 ? "#6d4dff" : clamped >= 40 ? "#f59e0b" : "#ef4444"

  return (
    <div className={cn("relative inline-flex items-center justify-center", className)} style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={radius} stroke="currentColor" strokeWidth={strokeWidth} fill="none" className="text-ink-100 dark:text-ink-800" />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={color}
          strokeWidth={strokeWidth}
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 0.6s ease" }}
        />
      </svg>
      <div className="absolute flex flex-col items-center">
        <span className="font-display text-[22px] font-semibold text-ink-950 dark:text-white">{Math.round(clamped)}</span>
        {label && <span className="text-[10.5px] text-ink-400">{label}</span>}
      </div>
    </div>
  )
}
