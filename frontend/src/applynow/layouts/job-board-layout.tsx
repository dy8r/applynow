import React from "react";
import { Link, useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  MenuIcon,
  XIcon,
  MoonIcon,
  SunIcon,
  DraftingCompassIcon
} from "lucide-react";
import { useState, useEffect } from "react";
import AlertDialog from "../components/alert-dialog";
import { useAnalytics } from "@/applynow/hooks/use-analytics"

interface JobBoardLayoutProps {
  children: React.ReactNode;
}

export default function JobBoardLayout({ children }: JobBoardLayoutProps) {
  useAnalytics(window.location.pathname)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const location = useLocation();

  // Check system preference and localStorage on mount
  useEffect(() => {
    // Check if user has a theme preference in localStorage
    const storedTheme = localStorage.getItem("theme");

    if (
      storedTheme === "dark" ||
      (!storedTheme &&
        window.matchMedia("(prefers-color-scheme: dark)").matches)
    ) {
      setIsDarkMode(true);
      document.documentElement.classList.add("dark");
    } else {
      setIsDarkMode(false);
      document.documentElement.classList.remove("dark");
    }
  }, []);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const toggleDarkMode = () => {
    if (isDarkMode) {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
      setIsDarkMode(false);
    } else {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
      setIsDarkMode(true);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-background dark:bg-slate-900">
      {/* Header */}
      <header className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 dark:bg-slate-900/95 dark:border-slate-800">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-6">
            <Link to="/" className="flex items-center gap-2">
              <DraftingCompassIcon className="h-6 w-6 text-green-600 dark:text-green-500" />

              <span className="font-bold text-xl dark:text-white">
                ApplyNow
              </span>
            </Link>

            <nav className="hidden md:flex items-center gap-6">
            <Link
              to="/"
              className={cn(
                "text-sm font-medium transition-colors",
                location.pathname === "/"
                  ? "text-green-600 dark:text-green-400"
                  : "text-muted-foreground hover:text-green-600 dark:text-gray-400 dark:hover:text-green-500"
              )}
            >
              Browse Jobs
            </Link>

            <Link
              to="/resources"
              className={cn(
                "text-sm font-medium transition-colors",
                location.pathname === "/resources"
                  ? "text-green-600 dark:text-green-400"
                  : "text-muted-foreground hover:text-green-600 dark:text-gray-400 dark:hover:text-green-500"
              )}
            >
              Resources
            </Link>

            </nav>
          </div>

          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleDarkMode}
              className="rounded-full"
              aria-label="Toggle dark mode"
            >
              {isDarkMode ? (
                <SunIcon className="h-5 w-5 text-yellow-500" />
              ) : (
                <MoonIcon className="h-5 w-5 text-gray-700" />
              )}
            </Button>

            <div className="hidden md:flex items-center gap-4">
              <AlertDialog />
            </div>

            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
              onClick={toggleMobileMenu}
            >
              {isMobileMenuOpen ? (
                <XIcon className="h-5 w-5" />
              ) : (
                <MenuIcon className="h-5 w-5" />
              )}
            </Button>
          </div>
        </div>
      </header>

      {/* Mobile menu */}
      <div
        className={cn(
          "fixed inset-0 top-16 z-30 bg-background dark:bg-slate-900 md:hidden transform transition-transform duration-300 ease-in-out",
          isMobileMenuOpen ? "translate-x-0" : "translate-x-full"
        )}
      >
        <nav className="container py-6 flex flex-col gap-4">
          <Link
            to="/"
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-md hover:bg-accent dark:hover:bg-slate-800"
            onClick={() => setIsMobileMenuOpen(false)}
          >
            Browse Jobs
          </Link>
          <Link
            to="/resources"
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-md hover:bg-accent dark:hover:bg-slate-800"
            onClick={() => setIsMobileMenuOpen(false)}
          >
            Resources
          </Link>

          <div className="border-t my-4 dark:border-slate-800"></div>

          <AlertDialog/>
        </nav>
      </div>

      {/* Main content */}
      <main className="flex-1">
          {children}
      </main>


      {/* Footer */}
      <footer className="border-t py-8 bg-background dark:bg-slate-900 dark:border-slate-800">
        <div className="container">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <Link to="/" className="flex items-center gap-2 mb-4">
                <DraftingCompassIcon className="h-5 w-5 text-green-600 dark:text-green-500" />

                <span className="font-bold text-lg dark:text-white">
                  ApplyNow
                </span>
              </Link>
              <p className="text-sm text-muted-foreground dark:text-gray-400">
                Be the first to know about new opportunities in Winnipeg's tech scene and find your dream job.
              </p>
            </div>

            <div>
              <h3 className="font-medium mb-3 dark:text-gray-200">
                For Job Seekers
              </h3>
              <ul className="space-y-2">
                <li>
                  <Link
                    to="/"
                    className="text-sm text-muted-foreground hover:text-green-600 dark:text-gray-400 dark:hover:text-green-500"
                  >
                    Browse Jobs
                  </Link>
                </li>
              </ul>
            </div>

            <div>
              <h3 className="font-medium mb-3 dark:text-gray-200">For Everyone Else</h3>
              <ul className="space-y-2">
                <li>
                  <Link
                    to="/resources"
                    className="text-sm text-muted-foreground hover:text-green-600 dark:text-gray-400 dark:hover:text-green-500"
                  >
                    Contact Me
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
