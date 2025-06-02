import React, { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import {
  FilterIcon,
  XIcon,
  CheckIcon,
  SlidersIcon,
  MapPinIcon,
  LaptopIcon
} from "lucide-react";


interface FilterOption {
  id: string;
  label: string;
  count?: number;
}

interface FilterGroupProps {
  title: string;
  options: FilterOption[];
  selectedOptions: string[];
  onChange: (optionId: string) => void;
}

function FilterGroup({
  title,
  options,
  selectedOptions,
  onChange,
}: FilterGroupProps) {
  return (
    <AccordionItem value={title.toLowerCase().replace(/\s+/g, "-")}>
      <AccordionTrigger className="text-sm font-medium hover:no-underline">
        {title}
      </AccordionTrigger>
      <AccordionContent>
        <div className="space-y-2 pt-1">
          {options.map((option) => (
            <div key={option.id} className="flex items-center space-x-2">
              <Checkbox
                id={`filter-${option.id}`}
                checked={selectedOptions.includes(option.id)}
                onCheckedChange={() => onChange(option.id)}
              />

              <Label
                htmlFor={`filter-${option.id}`}
                className="flex-1 text-sm cursor-pointer flex justify-between"
              >
                <span>{option.label}</span>
                {option.count !== undefined && (
                  <span className="text-muted-foreground text-xs">
                    ({option.count})
                  </span>
                )}
              </Label>
            </div>
          ))}
        </div>
      </AccordionContent>
    </AccordionItem>
  );
}

interface FilterSidebarProps {
  seniority: FilterOption[];
  jobTypes: FilterOption[];
  workModels: FilterOption[];
  departments: FilterOption[];
  industries: FilterOption[];
  onFilterChange: (filterType: string, selectedOptions: string[]) => void;
  onWinnipegOnlyChange: (isWinnipegOnly: boolean) => void;
  className?: string;
  isWinnipegOnlyProp?: boolean;
  clearFiltersToggle?: boolean;
  isSweOnlyProp?: boolean;
  onSweOnlyChange: (isSweOnly: boolean) => void;
}

export default function FilterSidebar({
  seniority,
  jobTypes,
  workModels,
  isWinnipegOnlyProp = true,
  isSweOnlyProp = false,
  onSweOnlyChange,
  departments,
  industries,
  onFilterChange,
  onWinnipegOnlyChange,
  className,
  clearFiltersToggle = true,
  
}: FilterSidebarProps) {
  const [selectedSeniority, setSelectedSeniority] = useState<string[]>([]);
  const [selectedJobTypes, setSelectedJobTypes] = useState<string[]>([]);
  const [selectedWorkModels, setSelectedWorkModels] = useState<string[]>([]);
  const [selectedDepartments, setSelectedDepartments] = useState<string[]>([]);
  const [selectedIndustries, setSelectedIndustries] = useState<string[]>([]);
  const [isWinnipegOnly, setIsWinnipegOnly] = useState(isWinnipegOnlyProp);
  const [isSweOnly, setIsSweOnly] = useState(isSweOnlyProp);
  const [isMobileFilterOpen, setIsMobileFilterOpen] = useState(false);

  const handleSeniorityChange = (seniorityId: string) => {
    const newSelection = selectedSeniority.includes(seniorityId)
      ? selectedSeniority.filter((id) => id !== seniorityId)
      : [...selectedSeniority, seniorityId];

    setSelectedSeniority(newSelection);
    onFilterChange("seniority", newSelection);
  };

  const handleJobTypeChange = (typeId: string) => {
    const newSelection = selectedJobTypes.includes(typeId)
      ? selectedJobTypes.filter((id) => id !== typeId)
      : [...selectedJobTypes, typeId];

    setSelectedJobTypes(newSelection);
    onFilterChange("jobTypes", newSelection);
  };

  const handleWorkModelChange = (modelId: string) => {
    const newSelection = selectedWorkModels.includes(modelId)
      ? selectedWorkModels.filter((id) => id !== modelId)
      : [...selectedWorkModels, modelId];

    setSelectedWorkModels(newSelection);
    onFilterChange("workModels", newSelection);
  };

  const handleDepartmentChange = (deptId: string) => {
    const newSelection = selectedDepartments.includes(deptId)
      ? selectedDepartments.filter((id) => id !== deptId)
      : [...selectedDepartments, deptId];

    setSelectedDepartments(newSelection);
    onFilterChange("department", newSelection);
  };

  const handleIndustryChange = (industryId: string) => {
    const newSelection = selectedIndustries.includes(industryId)
      ? selectedIndustries.filter((id) => id !== industryId)
      : [...selectedIndustries, industryId];

    setSelectedIndustries(newSelection);
    onFilterChange("industries", newSelection);
  };

  const handleWinnipegOnlyChange = () => {
    const newValue = !isWinnipegOnly;
    setIsWinnipegOnly(newValue);
    onWinnipegOnlyChange(newValue);
  };

  const handleSweOnlyChange = () => {
    const newValue = !isSweOnly;
    setIsSweOnly(newValue);
    onSweOnlyChange(newValue);
  };

  const clearAllFilters = () => {
    setSelectedSeniority([]);
    setSelectedJobTypes([]);
    setSelectedWorkModels([]);
    setSelectedDepartments([]);
    setSelectedIndustries([]);
    setIsWinnipegOnly(false);
    setIsSweOnly(false);

    onFilterChange("seniority", []);
    onFilterChange("jobTypes", []);
    onFilterChange("workModels", []);
    onFilterChange("departments", []);
    onFilterChange("industries", []);
    onWinnipegOnlyChange(false);
  };

  const totalSelectedFilters =
    selectedSeniority.length +
    selectedJobTypes.length +
    selectedWorkModels.length +
    selectedDepartments.length +
    selectedIndustries.length +
    (isWinnipegOnly ? 1 : 0)
    + (isSweOnly ? 1 : 0);

  const filterContent = (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold flex items-center gap-2">
          <FilterIcon className="h-4 w-4" />
          Filters
        </h2>
        {totalSelectedFilters > 0 && (
          <Button
            variant="ghost"
            size="sm"
            onClick={clearAllFilters}
            className="h-8 text-xs"
          >
            Clear all
            <XIcon className="ml-1 h-3 w-3" />
          </Button>
        )}
      </div>
      
      <div>
      <div className="bg-green-50 dark:bg-green-900/20 p-3 rounded-lg mb-2">
        <div className="flex items-center space-x-2">
          <Checkbox
            id="filter-winnipeg-only"
            checked={isWinnipegOnly}
            onCheckedChange={handleWinnipegOnlyChange}
          />

          <Label
            htmlFor="filter-winnipeg-only"
            className="flex items-center gap-1.5 text-sm font-medium cursor-pointer"
          >
            <MapPinIcon className="h-4 w-4 text-green-600 dark:text-green-500" />
            Winnipeg Only
          </Label>
        </div>
      </div>

      <div className="bg-purple-50 dark:bg-purple-900/20 p-3 rounded-lg mb-0">
        <div className="flex items-center space-x-2">
          <Checkbox
            id="filter-winnipeg-only"
            checked={isSweOnly}
            onCheckedChange={handleSweOnlyChange}
          />

          <Label
            htmlFor="filter-winnipeg-only"
            className="flex items-center gap-1.5 text-sm font-medium cursor-pointer"
          >
            <LaptopIcon className="h-4 w-4 text-purple-600 dark:text-purple-500" />
            SWE Only
          </Label>
        </div>
      </div>
      </div>


      <Accordion
        type="multiple"
        defaultValue={["seniority", "job-type", "work-model"]}
      >

        {departments.length > 0 && (
          <FilterGroup
        title="Department"
        options={departments}
        selectedOptions={selectedDepartments}
        onChange={handleDepartmentChange}
          />
        )}

        {seniority.length > 0 && (
          <FilterGroup
        title="Seniority"
        options={seniority}
        selectedOptions={selectedSeniority}
        onChange={handleSeniorityChange}
          />
        )}

        {workModels.length > 0 && (
          <FilterGroup
        title="Work Model"
        options={workModels}
        selectedOptions={selectedWorkModels}
        onChange={handleWorkModelChange}
          />
        )}

        {jobTypes.length > 0 && (
          <FilterGroup
        title="Job Type"
        options={jobTypes}
        selectedOptions={selectedJobTypes}
        onChange={handleJobTypeChange}
          />
        )}

        {industries.length > 0 && (
          <FilterGroup
        title="Industry"
        options={industries}
        selectedOptions={selectedIndustries}
        onChange={handleIndustryChange}
          />
        )}
      </Accordion>
    </div>
  );

  // Mobile filter button and drawer
  const mobileFilterButton = (
    <div className="md:hidden fixed bottom-4 right-4 z-50">
      <Button
        onClick={() => setIsMobileFilterOpen(true)}
        className="rounded-full h-12 w-12 shadow-lg bg-green-600 hover:bg-green-700 dark:bg-green-700 dark:hover:bg-green-600"
      >
        <SlidersIcon className="h-5 w-5" />

        {totalSelectedFilters > 0 && (
          <span className="absolute -top-1 -right-1 bg-white text-green-700 rounded-full h-5 w-5 flex items-center justify-center text-xs font-bold">
            {totalSelectedFilters}
          </span>
        )}
      </Button>
    </div>
  );

  const mobileFilterDrawer = (
    <div
      className={cn(
        "fixed inset-0 z-50 bg-background dark:bg-gray-900 transform transition-transform duration-300 ease-in-out md:hidden",
        isMobileFilterOpen ? "translate-y-0" : "translate-y-full"
      )}
    >
      <div className="flex flex-col h-full">
        <div className="flex items-center justify-between p-4 border-b dark:border-gray-800">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <FilterIcon className="h-4 w-4" />
            Filters
          </h2>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setIsMobileFilterOpen(false)}
          >
            <XIcon className="h-5 w-5" />
          </Button>
        </div>

        <div className="flex-1 overflow-y-auto p-4">{filterContent}</div>

        <div className="p-4 border-t bg-background dark:bg-gray-900 dark:border-gray-800">
          <div className="flex gap-3">
            <Button
              variant="outline"
              className="flex-1"
              onClick={clearAllFilters}
            >
              Clear all
            </Button>
            <Button
              className="flex-1 gap-1 bg-green-600 hover:bg-green-700 dark:bg-green-700 dark:hover:bg-green-600"
              onClick={() => setIsMobileFilterOpen(false)}
            >
              Apply Filters
              <CheckIcon className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );


  useEffect(() => {
    if (clearFiltersToggle) {
      clearAllFilters();
    }
  }, [clearFiltersToggle]);

  return (
    <>
      <div
        className={cn(
          "hidden md:block sticky top-24 h-[calc(100vh-6rem)] overflow-y-auto pb-8 scrollbar-hide",
          className
        )}
      >
        {filterContent}
      </div>

      {mobileFilterButton}
      {mobileFilterDrawer}
    </>
  );
}
