import React, { useState } from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { SearchIcon, MapPinIcon, XIcon, ArrowRightIcon } from "lucide-react";

interface SearchBarProps {
  onSearch: (query: string, location: string) => void;
  className?: string;
  initialQuery?: string;
  initialLocation?: string;
}

export default function SearchBar({
  onSearch,
  className,
  initialQuery = "",
  initialLocation = "",
}: SearchBarProps) {
  const [query, setQuery] = useState(initialQuery);
  const [location, setLocation] = useState(initialLocation);
  const [isFocused, setIsFocused] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(query.trim(), location.trim());
  };

  const clearQuery = () => {
    setQuery("");
  };

  const clearLocation = () => {
    setLocation("");
  };

  return (
    <form
      onSubmit={handleSubmit}
      className={cn(
        "flex flex-col md:flex-row gap-2 w-full transition-all",
        isFocused ? "scale-[1.01]" : "scale-100",
        className
      )}
    >
      <div className="relative flex-1">
        <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />

        <Input
          type="text"
          placeholder="Job title, keywords, or company"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          className="pl-9 pr-8 h-12 rounded-md"
        />

        {query && (
          <Button
            type="button"
            variant="ghost"
            size="icon"
            className="absolute right-1 top-1/2 transform -translate-y-1/2 h-8 w-8 text-muted-foreground hover:text-foreground"
            onClick={clearQuery}
          >
            <XIcon className="h-4 w-4" />
          </Button>
        )}
      </div>

      <div className="relative md:w-1/3">
        <MapPinIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />

        <Input
          type="text"
          placeholder="Location (optional)"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          className="pl-9 pr-8 h-12 rounded-md"
        />

        {location && (
          <Button
            type="button"
            variant="ghost"
            size="icon"
            className="absolute right-1 top-1/2 transform -translate-y-1/2 h-8 w-8 text-muted-foreground hover:text-foreground"
            onClick={clearLocation}
          >
            <XIcon className="h-4 w-4" />
          </Button>
        )}
      </div>

      <Button type="submit" className="h-12 px-6 gap-2">
        Search
        <ArrowRightIcon className="h-4 w-4" />
      </Button>
    </form>
  );
}
