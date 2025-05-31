import React, { useState, useEffect } from "react";
import { getJobPostings, getFilterOptions, JobPosting } from "@/applynow/data/job-postings-data";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
  ListIcon,
  GridIcon,
  FilterIcon,
  XIcon,
} from "lucide-react";

import JobCard from "@/applynow/components/job-card";
import FilterSidebar from "@/applynow/components/filter-sidebar";
import Pagination from "@/applynow/components/pagination";

interface Filter {
  id: string;
  label: string;
  count: number;
}

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

const JobCardSkeleton = () => (
  <div className="animate-pulse rounded-lg bg-muted/30 p-6 space-y-4">
    <div className="h-4 bg-muted-foreground/50 rounded w-1/2" />
    <div className="h-3 bg-muted-foreground/30 rounded w-1/3" />
    <div className="h-3 bg-muted-foreground/30 rounded w-full" />
    <div className="h-3 bg-muted-foreground/30 rounded w-5/6" />
  </div>
);

export default function JobDashboard() {
  const [jobs, setJobs] = useState<JobPosting[]>([]);
  const [activeFilters, setActiveFilters] = useState<{
    seniority: string[];
    jobTypes: string[];
    workModels: string[];
    department: string[];
    industries: string[];
  }>({
    seniority: [],
    jobTypes: [],
    workModels: [],
    department: [],
    industries: [],
  });

  const [isLoading, setIsLoading] = useState(false);

  const [totalActiveFilters, setTotalActiveFilters] = useState(0);
  const [clearFiltersToggle, setClearFiltersToggle] = useState(false);

  const [isWinnipegOnly, setIsWinnipegOnly] = useState(true); // default to Winnipeg only
  const [isSweOnly, setIsSweOnly] = useState(true); // default to SWE only
  

  const [viewMode, setViewMode] = useState<"list" | "grid">("list");
  const [availableFilters, setAvailableFilters] = useState<{
    seniority: Filter[];
    jobTypes: Filter[];
    workModels: Filter[];
    departments: Filter[];
    industries: Filter[];
  }>({
    seniority: [],
    jobTypes: [],
    workModels: [],
    departments: [],
    industries: [],
  });

  const [currentPage, setCurrentPage] = useState(1);
  const jobsPerPage = 10;
  const [totalPages, setTotalPages] = useState(0);
  const [indexOfLastJob, setIndexOfLastJob] = useState(0);
  const [indexOfFirstJob, setIndexOfFirstJob] = useState(0);
  const [totalJobs, setTotalJobs] = useState(0);


  const handleFilterChange = (
    filterType: string,
    selectedOptions: string[]
  ) => {
    const updated = {
      ...activeFilters,
      [filterType]: selectedOptions,
    };
    console.log("Updated filters:", updated);
    console.log("Selected options:", selectedOptions);

    setActiveFilters(updated);

    const newActiveFilters = Object.values(updated)
      .flat()
      .filter((v) => typeof v === "string" || (v && typeof v === "object" && "id" in v))
      .length;
    setTotalActiveFilters(newActiveFilters);

    setCurrentPage(1);
  };

  const handleWinnipegOnlyChange = (value: boolean) => {
    setIsWinnipegOnly(value);
    setCurrentPage(1);
  };

  const handleSweOnlyChange = (value: boolean) => {
    setIsSweOnly(value);
    setCurrentPage(1); 
  }

  const toggleViewMode = () => {
    setViewMode(viewMode === "list" ? "grid" : "list");
  };



  const clearAllFilters = () => {
    setActiveFilters({
      seniority: [],
      jobTypes: [],
      workModels: [],
      department: [],
      industries: [],
    });
    setIsWinnipegOnly(false);
    setIsSweOnly(false);
    setTotalActiveFilters(0);
    setCurrentPage(1);
    setClearFiltersToggle(!clearFiltersToggle);
  };


  const handlePageChange = (pageNumber: number) => {
    setCurrentPage(pageNumber);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const fetchJobs = async () => {
    try {
      setIsLoading(true);
      const queryParams = new URLSearchParams();

      queryParams.set("limit", jobsPerPage.toString());
      queryParams.set("offset", ((currentPage - 1) * jobsPerPage).toString());
      if (isWinnipegOnly) queryParams.set("is_winnipeg", "true");
      if (isSweOnly) queryParams.set("is_swe", "true");

      Object.entries(activeFilters).forEach(([key, values]) => {
        if (Array.isArray(values) && values.length > 0) {
          values.forEach((v: string) => {
            if (v) {
              queryParams.append(key, v);
            }
          });
        }
      });


      const data = await getJobPostings(`?${queryParams.toString()}`);

      setJobs(data.data);
      setTotalPages(Math.ceil(data.total / jobsPerPage));
      setIndexOfLastJob(currentPage * jobsPerPage);
      setIndexOfFirstJob(currentPage * jobsPerPage - jobsPerPage);
      setTotalJobs(data.total);
      setIsLoading(false); 
    } catch (err) {
      setIsLoading(false);
      console.error("Error fetching jobs:", err);
    }
  };


  useEffect(() => {
    const fetchFilterOptions = async () => {
      try {
        const data = await getFilterOptions();
        setAvailableFilters(data);
      } catch (err) {
        console.error("Error fetching filter options:", err);
      }
    };

    fetchJobs();
    fetchFilterOptions();
  }, []);

  useEffect(() => {
    // Re-fetch jobs whenever filters or pagination changes
    fetchJobs();
  }
    , [activeFilters, isWinnipegOnly, currentPage, availableFilters, isSweOnly]);

  return (
    <div className="min-h-screen">
      {/* Hero section */}
      <section className="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-slate-900 py-12">
        <div className="container">
          <div className="max-w-3xl mx-auto text-center mb-8">
            <h1 className="text-3xl md:text-4xl font-bold mb-4 dark:text-white">
              Find Your Perfect Job
            </h1>
            <p className="text-muted-foreground text-lg dark:text-gray-300">
              Browse jobs from top Winnipeg tech companies
            </p>
          </div>
        </div>
      </section>

      {/* Main content */}
      <section className="container py-8">
        <div className="flex flex-col md:flex-row gap-8">
          {/* Sidebar with filters */}
          <aside className="md:w-64 scrollbar-hide">
            <FilterSidebar
              seniority={availableFilters.seniority}
              jobTypes={availableFilters.jobTypes}
              workModels={availableFilters.workModels}
              isWinnipegOnlyProp={isWinnipegOnly}
              departments={availableFilters.departments}
              industries={availableFilters.industries}
              onFilterChange={handleFilterChange}
              onWinnipegOnlyChange={handleWinnipegOnlyChange}
              clearFiltersToggle={clearFiltersToggle}
              isSweOnlyProp={isSweOnly}
              onSweOnlyChange={handleSweOnlyChange}
            />
          </aside>

          {/* Job listings */}
          <div className="flex-1">
            {/* Results header */}
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
              <div>
                <h2 className="text-xl font-semibold dark:text-white">
                  {totalJobs}{" "}
                  {totalJobs === 1 ? "Job" : "Jobs"} Found
                </h2>
                {totalActiveFilters > 0 && (
                  <div className="text-sm text-muted-foreground mt-1 flex items-center gap-2">
                    <span>Filtered results</span>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={clearAllFilters}
                      className="h-7 text-xs gap-1 px-2"
                    >
                      Clear all
                      <XIcon className="h-3 w-3" />
                    </Button>
                  </div>
                )}
              </div>

              <div className="flex items-center gap-2 self-end sm:self-auto">
                <Separator orientation="vertical" className="h-8 hidden sm:block" />

                <Button
                  variant="ghost"
                  size="icon"
                  onClick={toggleViewMode}
                  className="h-8 w-8 hidden sm:block"
                  title={viewMode === "list" ? "Grid view" : "List view"}
                >
                  {viewMode === "list" ? (
                  <GridIcon className="h-4 w-4" />
                  ) : (
                  <ListIcon className="h-4 w-4" />
                  )}
                </Button>
              </div>
            </div>

            {/* Job listings */}
            {isLoading ? (
              <div
                className={`grid gap-4 ${viewMode === "grid" ? "grid-cols-1 md:grid-cols-2" : "grid-cols-1"
                  }`}
              >
                {Array.from({ length: jobsPerPage }).map((_, index) => (
                  <JobCardSkeleton key={index} />
                ))}
              </div>
            ) : totalJobs > 0 ? (
              <div className="space-y-6">
                <div
                  className={`grid gap-4 ${viewMode === "grid"
                      ? "grid-cols-1 md:grid-cols-2"
                      : "grid-cols-1"
                    }`}
                >
                  {jobs.map((job) => (
                    <JobCard
                      key={job.id}
                      id={job.id}
                      title={job.title}
                      company={job.company}
                      description={job.description_html}
                      experienceLevel={SENIORITY_BACK_TO_FRONT_MAP[job.seniority] as 'Entry' | 'Mid' | 'Senior' | 'Lead'}
                      location={job.location}
                      locationType={WORK_MODEL_MAP[job.work_model]}
                      techStack={job.technologies}
                      datePosted={job.date_added}
                      department={job.department}
                      industry={job.industry}
                    />
                  ))}
                </div>

                {/* Pagination */}
                {totalJobs > jobsPerPage && (
                  <div className="mt-8 flex flex-col items-center gap-2">
                    <Pagination
                      currentPage={currentPage}
                      totalPages={totalPages}
                      onPageChange={handlePageChange}
                    />

                    <p className="text-sm text-muted-foreground mt-2">
                      Showing {indexOfFirstJob + 1}-
                      {Math.min(indexOfLastJob, totalJobs)} of{" "}
                      {totalJobs} jobs
                    </p>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center py-12 bg-muted/30 rounded-lg dark:bg-slate-800/30">
                <FilterIcon className="h-12 w-12 mx-auto text-muted-foreground mb-4" />

                <h3 className="text-xl font-medium mb-2 dark:text-white">
                  No jobs found
                </h3>
                <p className="text-muted-foreground mb-6 dark:text-gray-400">
                  Try adjusting your search or filter criteria
                </p>
                <Button
                  onClick={clearAllFilters}
                  className="bg-green-600 hover:bg-green-700 dark:bg-green-700 dark:hover:bg-green-600"
                >
                  Clear all filters
                </Button>
              </div>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
