import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { getJobPostingById, JobPosting } from "@/applynow/data/job-postings-data";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import {
  ArrowLeftIcon,
  CalendarIcon,
  BriefcaseIcon,
  DollarSignIcon,
  ExternalLinkIcon,
  BookmarkIcon,
  ShareIcon,
  CheckIcon,
  MapPinIcon,
} from "lucide-react";
import CompanyBadge from "@/applynow/components/company-badge";
import TechBadge from "@/applynow/components/tech-badge";
import ExperienceLevelBadge from "@/applynow/components/experience-level-badge";
import LocationBadge from "@/applynow/components/location-badge";


const SENIORITY_BACK_TO_FRONT_MAP: Record<string, string> = {
  entry: "Entry",
  mid: "Mid",
  senior: "Senior",
  lead: "Lead",
};

const WORK_MODEL_MAP: Record<string, string> = {
  remote: "Remote",
  'on-site': "On-site",
  hybrid: "Hybrid",
};


export default function JobDetail() {
  const { id = "" } = useParams();
  const [isLoading, setIsLoading] = useState(true);
  const [shareText, setShareText] = useState("Share");

  // Find the job posting by ID
  const [job, setJob] = useState<JobPosting | null>(null);

  const handleShareClick = () => {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(window.location.href)
        .then(() => {
          setShareText("Link Copied!");
          setTimeout(() => setShareText("Share"), 2000);
        })
        .catch((error) => {
          console.error("Error copying link:", error);
        });
    } else {
      alert("Sharing not supported in this browser.");
    }
  };

  useEffect(() => {
    const fetchJob = async () => {
      try {
        setIsLoading(true);
        const jobData = await getJobPostingById(id);
        setJob(jobData);
        setIsLoading(false);
      } catch (error) {
        console.error("Failed to fetch job posting:", error);
        setJob(null); // Set to null if not found
        setIsLoading(false);
      }
    };
    if (id) {
      fetchJob();
    }
  }, [id]);


  // Format the date
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    }).format(date);
  };

  // Format salary range
  const formatSalary = (
    min: number | null,
    max: number | null
  ) => {
    const formatNumber = (num: number) => {
      return num >= 1000 ? `${(num / 1000).toFixed(0)}k` : num;
    };

    if (min == null && max == null) {
      return "N/A";
    }

    if (min == null) {
      return `Up to $${formatNumber(max!)} Annually`;
    }

    if (max == null) {
      return `From $${formatNumber(min)} Annually`;
    }

    return `$${formatNumber(min)} - $${formatNumber(max)} Annually`;
  };


  if (isLoading) {
    return (
      <div className="container py-8 animate-pulse">
        {/* Back button placeholder */}
        <div className="mb-6 h-6 w-32 bg-muted rounded" />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main content skeleton */}
          <div className="lg:col-span-2 space-y-8">
            {/* Header section */}
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <div className="h-8 w-48 bg-muted rounded" />
                <div className="h-4 w-24 bg-muted rounded" />
              </div>
              <div className="h-6 w-3/4 bg-muted rounded" />
              <div className="flex gap-2 flex-wrap">
                <div className="h-5 w-24 bg-muted rounded" />
                <div className="h-5 w-24 bg-muted rounded" />
                <div className="h-5 w-36 bg-muted rounded" />
              </div>
            </div>

            {/* Description */}
            <div className="space-y-2">
              <div className="h-5 w-48 bg-muted rounded" />
              <div className="h-4 w-full bg-muted rounded" />
              <div className="h-4 w-full bg-muted rounded" />
              <div className="h-4 w-5/6 bg-muted rounded" />
            </div>

            {/* Tech stack */}
            <div className="space-y-2">
              <div className="h-5 w-36 bg-muted rounded" />
              <div className="flex gap-2 flex-wrap">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="h-6 w-20 bg-muted rounded" />
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar skeleton */}
          <div className="space-y-6">
            {/* Apply card */}
            <div className="border rounded-lg p-6 space-y-4">
              <div className="h-5 w-40 bg-muted rounded" />
              <div className="h-10 w-full bg-muted rounded" />
              <div className="h-8 w-24 bg-muted rounded" />
            </div>

            {/* Job details card */}
            <div className="border rounded-lg p-6 space-y-4">
              <div className="h-5 w-36 bg-muted rounded" />
              {[...Array(5)].map((_, i) => (
                <div key={i}>
                  <div className="h-4 w-24 bg-muted rounded mb-1" />
                  <div className="h-4 w-36 bg-muted rounded" />
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // If job not found, show error
  if (!job && !isLoading) {
    return (
      <div className="container py-16 text-center">
        <h1 className="text-2xl font-bold mb-4">Job Not Found</h1>
        <p className="text-muted-foreground mb-8">
          The job posting you're looking for doesn't exist or has been removed.
        </p>
        <Button asChild>
          <Link to="/">
            <ArrowLeftIcon className="mr-2 h-4 w-4" />
            Back to Job Listings
          </Link>
        </Button>
      </div>
    );
  }



  return (
    <div className="container py-8">
      {/* Back button */}
      <div className="mb-6">
        <Button
          variant="ghost"
          asChild
          className="gap-2 pl-0 hover:pl-2 transition-all"
        >
          <Link to="/">
            <ArrowLeftIcon className="h-4 w-4" />
            Back to Job Listings
          </Link>
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main content */}
        <div className="lg:col-span-2 space-y-8">
          {/* Job header */}
          <div>
            <div className="flex items-start justify-between mb-4">
              <CompanyBadge
                name={job.company}
                size="lg"
              />

              <div className="flex items-center text-sm text-muted-foreground">
                <CalendarIcon className="h-4 w-4 mr-1" />

                <span>Posted on {formatDate(job.date_added)}</span>
              </div>
            </div>

            <h1 className="text-3xl font-bold mb-3">{job.title}</h1>

            <div className="flex flex-wrap gap-2 mb-6">
              {job.seniority && <ExperienceLevelBadge level={SENIORITY_BACK_TO_FRONT_MAP[job.seniority] as "Entry" | "Mid" | "Senior" | "Lead"} />}

              <LocationBadge
                type={WORK_MODEL_MAP[job.work_model] as "Remote" | "On-site" | "Hybrid"}
                location={job.location}
              />


              <div className="flex items-center text-xs bg-green-100 text-green-800 dark:bg-green-500/20 dark:text-green-400 rounded-md px-2 py-0.5">
                <DollarSignIcon className="h-3 w-3 mr-1" />

                <span>
                  {formatSalary(
                    job.salary_min,
                    job.salary_max,
                  )}
                </span>
              </div>

            </div>
          </div>

          {/* Job description */}
          <div>
            <h2 className="text-xl font-semibold mb-3">Job Description</h2>
            <div className="text-muted-foreground whitespace-pre-line mb-6" dangerouslySetInnerHTML={{ __html: job.description_html }} />
          </div>

          {/* Tech stack */}
          <div>
            <h2 className="text-xl font-semibold mb-3">Technologies</h2>
            <div className="flex flex-wrap gap-2">
              {job.technologies.map((tech, index) => (
                <TechBadge key={index} name={tech} />
              ))}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Apply card */}
          <Card>
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold mb-4">Apply for this job</h2>
              <Button
                className="w-full mb-4"
                size="lg"
                asChild
              >
                <a href={job.link} target="_blank" rel="noopener noreferrer">
                  Apply Now
                </a>
              </Button>
              <div className="flex justify-between">
                <Button
                  variant="outline"
                  size="sm"
                  className="gap-1"
                  onClick={handleShareClick}
                >
                  {shareText === "Share" &&
                    <ShareIcon className="h-4 w-4" />}
                  {shareText}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/*
          <Card>
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold mb-4">About the company</h2>
              <div className="flex items-center mb-4">
                <div className="h-16 w-16 rounded-md overflow-hidden mr-4 border">
                  <img
                    src={job.company.logo}
                    alt={`${job.company.name} logo`}
                    className="h-full w-full object-cover"
                  />
                </div>
                <div>
                  <h3 className="font-semibold">{job.company.name}</h3>
                  <p className="text-sm text-muted-foreground flex items-center mt-1">
                    <MapPinIcon className="h-3.5 w-3.5 mr-1" />

                    {job.company.location}
                  </p>
                </div>
              </div>
              <Separator className="my-4" />

              <Button variant="outline" className="w-full gap-1">
                View Company Profile
                <ExternalLinkIcon className="h-4 w-4" />
              </Button>
            </CardContent>
          </Card> */}

          {/* Job details */}
          <Card>
            <CardContent className="p-6">
              <h2 className="text-lg font-semibold mb-4">Job Details</h2>
              <div className="space-y-4">
                <div>
                  <h3 className="text-sm font-medium text-muted-foreground mb-1">
                    Job Type
                  </h3>
                  <p>{WORK_MODEL_MAP[job.work_model]}</p>
                </div>
                <div>
                  <h3 className="text-sm font-medium text-muted-foreground mb-1">
                    Experience Level
                  </h3>
                  <p>{SENIORITY_BACK_TO_FRONT_MAP[job.seniority]}</p>
                </div>
                <div>
                  <h3 className="text-sm font-medium text-muted-foreground mb-1">
                    Location
                  </h3>
                  <p>
                    {job.location}
                  </p>
                </div>
                {(job.salary_min || job.salary_max) && (
                  <div>
                    <h3 className="text-sm font-medium text-muted-foreground mb-1">
                      Salary Range
                    </h3>
                    <p>
                      CAD
                      {job.salary_min?.toLocaleString()} - {job.salary_max?.toLocaleString()}
                    </p>
                  </div>
                )}
                <div>
                  <h3 className="text-sm font-medium text-muted-foreground mb-1">
                    Posted On
                  </h3>
                  <p>{formatDate(job.date_added)}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
