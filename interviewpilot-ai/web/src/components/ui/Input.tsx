import { type InputHTMLAttributes, forwardRef } from "react"
import { cn } from "@/lib/utils"

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  error?: string
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, error, ...props }, ref) => (
    <div className="w-full">
      <input
        ref={ref}
        className={cn(
          "h-11 w-full rounded-xl border bg-white px-3.5 text-[14px] text-ink-950 placeholder:text-ink-400 transition focus:outline-none focus:ring-2 focus:ring-brand-400 focus:border-brand-400 dark:bg-ink-900 dark:text-white dark:border-ink-700",
          error ? "border-red-300 focus:ring-red-300 focus:border-red-400" : "border-ink-200",
          className
        )}
        {...props}
      />
      {error && <p className="mt-1.5 text-[12.5px] text-red-600">{error}</p>}
    </div>
  )
)
Input.displayName = "Input"

export const Label = ({ className, ...props }: React.LabelHTMLAttributes<HTMLLabelElement>) => (
  <label className={cn("mb-1.5 block text-[13px] font-medium text-ink-700 dark:text-ink-300", className)} {...props} />
)
