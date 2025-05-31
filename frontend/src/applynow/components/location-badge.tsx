import React from "react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { MapPinIcon, GlobeIcon, HomeIcon } from "lucide-react";

export type LocationType = "Remote" | "On-site" | "Hybrid";

interface LocationBadgeProps {
  type: LocationType;
  location?: string;
  className?: string;
  size?: "sm" | "md" | "lg";
}

export default function LocationBadge({
  type,
  location,
  className,
  size = "md",
}: LocationBadgeProps) {
  const colorClasses = {
    Remote:
      "bg-blue-100 text-blue-800 hover:bg-blue-100/80 dark:bg-blue-500/20 dark:text-blue-400",
    "On-site":
      "bg-amber-100 text-amber-800 hover:bg-amber-100/80 dark:bg-amber-500/20 dark:text-amber-400",
    Hybrid:
      "bg-purple-100 text-purple-800 hover:bg-purple-100/80 dark:bg-purple-500/20 dark:text-purple-400",
  };

  const sizeClasses = {
    sm: "text-xs px-2 py-0.5 gap-1",
    md: "text-sm px-2.5 py-0.5 gap-1.5",
    lg: "text-base px-3 py-1 gap-2",
  };

  const iconSizeClasses = {
    sm: "h-3 w-3",
    md: "h-3.5 w-3.5",
    lg: "h-4 w-4",
  };

  const LocationIcon = () => {
    switch (type) {
      case "Remote":
        return <GlobeIcon className={cn(iconSizeClasses[size])} />;

      case "On-site":
        return <MapPinIcon className={cn(iconSizeClasses[size])} />;

      case "Hybrid":
        return <HomeIcon className={cn(iconSizeClasses[size])} />;

      default:
        return <MapPinIcon className={cn(iconSizeClasses[size])} />;
    }
  };

  return (
    <Badge
      variant="secondary"
      className={cn(
        "rounded-md font-medium flex items-center",
        colorClasses[type],
        sizeClasses[size],
        className
      )}
    >
      <LocationIcon />

      <span>
        {type}
        {location ? ` · ${location}` : ""}
      </span>
    </Badge>
  );
}
