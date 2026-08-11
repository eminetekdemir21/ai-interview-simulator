import { cn } from "@/lib/utils"

interface AvatarProps {
  name: string
  size?: number
  className?: string
  src?: string
}

export function Avatar({ name, size = 36, className, src }: AvatarProps) {
  const initials = name
    .split(" ")
    .map((p) => p[0])
    .slice(0, 2)
    .join("")
    .toUpperCase()

  if (src) {
    return (
      <img
        src={src}
        alt={name}
        style={{ width: size, height: size }}
        className={cn("rounded-full object-cover", className)}
      />
    )
  }

  return (
    <div
      style={{ width: size, height: size, fontSize: size * 0.38 }}
      className={cn(
        "grad-bg flex items-center justify-center rounded-full font-semibold text-white shrink-0",
        className
      )}
    >
      {initials}
    </div>
  )
}
