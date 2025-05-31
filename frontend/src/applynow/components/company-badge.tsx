import React from "react";
import { cn } from "@/lib/utils";

interface CompanyBadgeProps {
  name: string;
  logo?: string;
  size?: "sm" | "md" | "lg";
  className?: string;
}

export default function CompanyBadge({
  name,
  logo,
  size = "md",
  className,
}: CompanyBadgeProps) {
  const sizeClasses = {
    sm: "h-6 w-6 text-xs",
    md: "h-8 w-8 text-sm",
    lg: "h-10 w-10 text-base",
  };

  const containerClasses = {
    sm: "text-xs py-1 px-2 gap-1.5",
    md: "text-sm py-1.5 px-3 gap-2",
    lg: "text-base py-2 px-4 gap-2.5",
  };

  // Extract first letter of each word for the fallback
  const fallbackText = name
    .split(" ")
    .map((word) => word[0])
    .join("")
    .toUpperCase()
    .substring(0, 2);

  return (
    <div
      className={cn(
        "flex items-center rounded-full bg-secondary/50 font-medium",
        containerClasses[size],
        className
      )}
    >
      <div
        className={cn(
          "relative rounded-full bg-white flex items-center justify-center overflow-hidden border border-border",
          sizeClasses[size]
        )}
      >
        {logo ? (
          <img
            src={logo}
            alt={`${name} logo`}
            className="h-full w-full object-cover"
            onError={(e) => {
              // If image fails to load, show fallback text
              (e.target as HTMLImageElement).style.display = "none";
              e.currentTarget.parentElement!.setAttribute(
                "data-fallback",
                fallbackText
              );
            }}
          />
        ) : (
            <span className="font-semibold text-neutral-900 dark:text-neutral-0">{fallbackText}</span>
        )}
      </div>
      <span className="truncate max-w-[150px]">{name}</span>
    </div>
  );
}
