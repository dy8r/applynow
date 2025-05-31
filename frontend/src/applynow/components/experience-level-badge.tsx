import React from "react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";

type ExperienceLevel = "Entry" | "Mid" | "Senior" | "Lead";

interface ExperienceLevelBadgeProps {
  level: ExperienceLevel;
  className?: string;
  size?: "sm" | "md" | "lg";
}

export default function ExperienceLevelBadge({
  level,
  className,
  size = "md",
}: ExperienceLevelBadgeProps) {
  const colorClasses = {
    Entry:
      "bg-green-100 text-green-800 hover:bg-green-100/80 dark:bg-green-500/20 dark:text-green-400",
    Mid: "bg-blue-100 text-blue-800 hover:bg-blue-100/80 dark:bg-blue-500/20 dark:text-blue-400",
    Senior:
      "bg-purple-100 text-purple-800 hover:bg-purple-100/80 dark:bg-purple-500/20 dark:text-purple-400",
    Lead: "bg-amber-100 text-amber-800 hover:bg-amber-100/80 dark:bg-amber-500/20 dark:text-amber-400",
  };

  const sizeClasses = {
    sm: "text-xs px-2 py-0.5",
    md: "text-sm px-2.5 py-0.5",
    lg: "text-base px-3 py-1",
  };

  return (
    <Badge
      variant="secondary"
      className={cn(
        "rounded-md font-medium",
        colorClasses[level],
        sizeClasses[size],
        className
      )}
    >
      {level}
    </Badge>
  );
}
