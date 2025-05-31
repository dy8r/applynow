import React from "react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";

interface TechBadgeProps {
  name: string;
  variant?: "default" | "outline" | "secondary";
  size?: "sm" | "md" | "lg";
  className?: string;
}

export default function TechBadge({
  name,
  variant = "secondary",
  size = "md",
  className,
}: TechBadgeProps) {
  const sizeClasses = {
    sm: "text-xs px-2 py-0.5",
    md: "text-sm px-2.5 py-0.5",
    lg: "text-base px-3 py-1",
  };

  return (
    <Badge
      variant={variant}
      className={cn(
        "rounded-md font-medium whitespace-nowrap",
        sizeClasses[size],
        className
      )}
    >
      {name}
    </Badge>
  );
}
