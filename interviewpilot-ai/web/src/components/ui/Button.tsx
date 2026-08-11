import { type ButtonHTMLAttributes, forwardRef } from "react"
import { cn } from "@/lib/utils"

type Variant = "primary" | "secondary" | "outline" | "ghost" | "danger"
type Size = "sm" | "md" | "lg"

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant
  size?: Size
}

const variantClasses: Record<Variant, string> = {
  primary:
    "grad-bg text-white shadow-soft hover:opacity-95 focus-visible:ring-brand-400",
  secondary:
    "bg-ink-900 text-white hover:bg-ink-800 dark:bg-white dark:text-ink-950 dark:hover:bg-ink-100 focus-visible:ring-ink-400",
  outline:
    "border border-ink-200 bg-white text-ink-900 hover:border-ink-300 hover:bg-ink-50 dark:bg-ink-900 dark:text-ink-50 dark:border-ink-700 dark:hover:bg-ink-800 focus-visible:ring-ink-300",
  ghost:
    "text-ink-600 hover:bg-ink-100 hover:text-ink-950 dark:text-ink-300 dark:hover:bg-ink-800 dark:hover:text-white focus-visible:ring-ink-300",
  danger:
    "bg-red-600 text-white hover:bg-red-700 focus-visible:ring-red-400",
}

const sizeClasses: Record<Size, string> = {
  sm: "h-8 px-3 text-[13px] rounded-lg gap-1.5",
  md: "h-10 px-4 text-[14px] rounded-xl gap-2",
  lg: "h-12 px-6 text-[15px] rounded-xl gap-2",
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center font-semibold transition-all duration-150 active:scale-[0.98] disabled:opacity-50 disabled:pointer-events-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 dark:focus-visible:ring-offset-ink-950",
          variantClasses[variant],
          sizeClasses[size],
          className
        )}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"
