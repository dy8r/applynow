const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export interface JobListResponse {
  data: JobPosting[];
  total: number;
  page: number;
  page_size: number;
}
export interface JobPosting {
  id: string;
  company: string;
  title: string;
  location: string;
  job_type: string;
  department: string;
  industry: string;
  work_model: string;
  seniority: string;
  technologies: string[]; // parsed from JSON
  is_winnipeg: boolean;
  salary_min: number | null;
  salary_max: number | null;
  min_experience: number | null;
  description_html: string;
  link: string;
  date_added: string; // ISO string
  last_seen: string;  // ISO string
}

export interface FilterOption {
  id: string;
  label: string;
  count: number;
}

export interface FiltersResponse {
  seniority: FilterOption[];
  jobTypes: FilterOption[];
  workModels: FilterOption[];
  departments: FilterOption[];
  industries: FilterOption[];
}

export const getJobPostings = async (
  query: string = ""
): Promise<JobListResponse> => {
  const res = await fetch(`${BASE_URL}/jobs/${query}`);
  if (!res.ok) {
    throw new Error("Failed to fetch job postings");
  }
  return res.json();
};

export const getCompanies = async (): Promise<string[]> => {
  const res = await fetch(`${BASE_URL}/companies`);
  if (!res.ok) throw new Error('Failed to fetch companies');
  const data = await res.json();
  return data;
};

export const getFilterOptions = async (): Promise<FiltersResponse> => {
  const res = await fetch(`${BASE_URL}/filters`);
  if (!res.ok) {
    throw new Error("Failed to fetch filter options");
  }
  return res.json();
};

export const getJobPostingById = async (
  id: string
): Promise<JobPosting> => {
  const res = await fetch(`${BASE_URL}/jobs/${id}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch job posting with id ${id}`);
  }
  return res.json();
}

export const sendAnalytics = async (path?: string): Promise<void> => {
  const actualPath = path || window.location.pathname
  console.log(actualPath)
  const res = await fetch(`${BASE_URL}/analytics`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ path: actualPath })
  });

  if (!res.ok) {
    console.warn("Analytics failed:", await res.text());
  }
}