import React from "react";
import { Link } from "react-router-dom";
import { cn } from "@/lib/utils";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  CalendarIcon,
  ArrowRightIcon,
} from "lucide-react";

import CompanyBadge from "@/applynow/components/company-badge";
import TechBadge from "@/applynow/components/tech-badge";
import ExperienceLevelBadge from "@/applynow/components/experience-level-badge";
import LocationBadge, { LocationType } from "@/applynow/components/location-badge";

interface JobCardProps {
  id: string;
  title: string;
  company: string
  description: string;
  experienceLevel: "Entry" | "Mid" | "Senior" | "Lead";
  locationType: string;
  location: string;
  isWinnipeg?: boolean;
  techStack: string[];
  datePosted: string;
  department?: string;
  industry?: string;
  className?: string;
}

export default function JobCard({
  id,
  title,
  company,
  description,
  experienceLevel,
  locationType,
  location,
  isWinnipeg = false,
  techStack,
  datePosted,
  className,
}: JobCardProps) {
  // Format the date posted
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    }).format(date);
  };

  // Calculate time since posting
  const getTimeSincePosting = (dateString: string) => {
    const postedDate = new Date(dateString);
    const currentDate = new Date();
    const diffTime = Math.abs(currentDate.getTime() - postedDate.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return "Today";
    if (diffDays === 1) return "Yesterday";
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;
    return `${Math.floor(diffDays / 365)} years ago`;
  };

  // Truncate description
  const truncateDescription = (text: string, maxLength: number = 160) => {
    // Remove HTML tags
    const plainText = text.replace(/<\/?[^>]+(>|$)/g, "");
    if (plainText.length <= maxLength) return plainText;
    return plainText.substring(0, maxLength) + "...";
  };

  return (
    <Card
      className={cn(
        "overflow-hidden hover:border-primary/50 transition-all",
        className
      )}
    >
      <CardContent className="p-6">
        <div className="flex flex-col space-y-4">
          {/* Company and date info */}
          <div className="flex justify-between items-start">
            <CompanyBadge name={company} />

            <div className="flex items-center text-xs text-muted-foreground">
              <CalendarIcon className="h-3 w-3 mr-1" />

              <span title={formatDate(datePosted)}>
                {getTimeSincePosting(datePosted)}
              </span>
            </div>
          </div>

          {/* Job title */}
          <Link to={`/job/${id}`} className="group">
            <h3 className="text-xl font-semibold group-hover:text-primary transition-colors">
              {title}
            </h3>
          </Link>

          {/* Job description */}
          <p className="text-muted-foreground text-sm">
            {truncateDescription(description)}
          </p>

          {/* Job details */}
          <div className="flex flex-wrap gap-2">
            {experienceLevel &&
              <ExperienceLevelBadge level={experienceLevel} />
            }
            <LocationBadge
              type={locationType as LocationType}
              location={location}
            />
          </div>

          {/* Tech stack */}
          <div className="flex flex-wrap gap-1.5 mt-2">
            {techStack.slice(0, 5).map((tech, index) => (
              <TechBadge key={index} name={tech} size="sm" variant="outline" />
            ))}
            {techStack.length > 5 && (
              <TechBadge
                name={`+${techStack.length - 5} more`}
                size="sm"
                variant="outline"
                className="bg-secondary/50"
              />
            )}
          </div>
        </div>
      </CardContent>
      <CardFooter className="px-6 py-4 bg-secondary/30 flex justify-between items-center">
        {/* <div className="flex items-center text-xs text-muted-foreground">
          <ClockIcon className="h-3 w-3 mr-1" />

          <span>Apply by {formatDate(datePosted)}</span>
        </div> */}
        <Button asChild size="sm" className="gap-1">
          <Link to={`/job/${id}`}>
            View Details
            <ArrowRightIcon className="h-3.5 w-3.5" />
          </Link>
        </Button>
      </CardFooter>
    </Card>
  );
}
