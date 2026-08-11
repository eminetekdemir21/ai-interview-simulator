import { type HTMLAttributes, forwardRef } from "react"
import { cn } from "@/lib/utils"

export const Card = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "rounded-2xl border border-ink-100 bg-white shadow-soft dark:border-ink-800 dark:bg-ink-900",
        className
      )}
      {...props}
    />
  )
)
Card.displayName = "Card"

export const CardHeader = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("p-5 pb-0 flex items-center justify-between", className)} {...props} />
  )
)
CardHeader.displayName = "CardHeader"

export const CardBody = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => <div ref={ref} className={cn("p-5", className)} {...props} />
)
CardBody.displayName = "CardBody"

export const CardTitle = forwardRef<HTMLHeadingElement, HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3
      ref={ref}
      className={cn("font-display text-[16px] font-semibold text-ink-950 dark:text-white", className)}
      {...props}
    />
  )
)
CardTitle.displayName = "CardTitle"

export const CardSubtitle = forwardRef<HTMLParagraphElement, HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <p ref={ref} className={cn("text-[13px] text-ink-500 dark:text-ink-400", className)} {...props} />
  )
)
CardSubtitle.displayName = "CardSubtitle"
