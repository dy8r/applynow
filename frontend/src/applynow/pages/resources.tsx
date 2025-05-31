import React from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  GithubIcon,
  LinkedinIcon,
  HeartIcon,
  CodeIcon,
  GlobeIcon,
} from "lucide-react";
import { Link } from "react-router-dom";

export default function Resources() {
  const storedTheme = localStorage.getItem("theme");
  return (
    <div className="container py-12 px-4 mx-auto max-w-5xl">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold tracking-tight mb-4 dark:text-white">
          Resources & About
        </h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Learn more about this project, me, and how you can use it for your own job search.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
        <Card className="flex flex-col h-full">
          <CardHeader>
            <CardTitle className="flex items-center">
              <CodeIcon className="mr-2 h-5 w-5 text-green-600 dark:text-green-500" />
              About This Project
            </CardTitle>
            <CardDescription>
              An open-source job board built for job seekers
            </CardDescription>
          </CardHeader>
          <CardContent className="flex-grow">
            <p className="mb-4">
                This job board is a fully open-source platform designed to help job seekers
                discover opportunities with speed and clarity. It features a clean,
                responsive interface built with React, TypeScript, Tailwind CSS, and
                Shadcn UI — providing modern filtering, smooth animations, and a mobile-first experience.
            </p>
            <p className="mb-4">
                The backend is powered by a high-performance Python stack using FastAPI,
                optimized for low-latency responses and scalable deployment. A custom Python-based job
                scraper continuously gathers listings from multiple sources, ensuring fresh
                data with minimal delay.
            </p>
            <p className="mb-4">
                Real-time alerts are delivered via a Telegram bot written in Python,
                allowing users to subscribe and be instantly notified about relevant new
                openings.
            </p>
            <p>
                The architecture is designed for performance, modularity, and extensibility — making it easy to
                fork, adapt, and integrate with additional sources or tools as needed.
            </p>
        </CardContent>

          <CardFooter>
            <Button
              variant="outline"
              className="w-full"
              onClick={() =>
                window.open(
                  "https://github.com/dy8r/applynow",
                  "_blank"
                )
              }
            >
              <GithubIcon className="mr-2 h-4 w-4" />
              View Source Code
            </Button>
          </CardFooter>
        </Card>

        <Card className="flex flex-col h-full">
          <CardHeader>
            <CardTitle className="flex items-center">
              <GlobeIcon className="mr-2 h-5 w-5 text-green-600 dark:text-green-500" />
              About The Creator
            </CardTitle>
            <CardDescription>
              Learn more about who built this project
            </CardDescription>
          </CardHeader>
          <CardContent className="flex-grow">
            <div className="flex items-center mb-4">
              <img
                src="https://github.com/dy8r.png"
                alt="Creator"
                className="h-16 w-16 rounded-full mr-4 border-2 border-green-600 dark:border-green-500"
              />

              <div>
                <h3 className="font-medium text-lg">Ivan Balkashynov</h3>
                <p className="text-muted-foreground">
                  Software Engineer with a spare weekend to build a job postings aggregator
                </p>
              </div>
            </div>
            <p className="mb-4">
            I have many friends who graduated from the University of Manitoba with a computer science degree, but are still struggling to land their first job. Winnipeg has a small tech ecosystem, with maybe 10–20 solid companies actively hiring, and opportunities can be hard to come by — especially for new grads.
            </p>
            <p className="mb-4">
            I built this job board to help level the playing field. It aggregates listings, filters them down to local and remote-friendly roles, and surfaces new opportunities quickly — because sometimes being early is half the battle.
            </p>
            <p>
            The platform is open source, fast, and built to scale. It's designed to make job hunting just a little easier for those trying to break into the industry, and to support the broader tech community here in Winnipeg.
            </p>

          </CardContent>
          <CardFooter>
            <Button
              variant="outline"
              className="w-full"
              onClick={() =>
                window.open("https://linkedin.com/in/balkashynov", "_blank")
              }
            >
              <LinkedinIcon className="mr-2 h-4 w-4" />
              Connect on LinkedIn
            </Button>
          </CardFooter>
        </Card>
      </div>

      <Card className="mb-12">
        <CardHeader>
          <CardTitle className="flex items-center">
            <HeartIcon className="mr-2 h-5 w-5 text-green-600 dark:text-green-500" />
            How You Can Contribute
          </CardTitle>
          <CardDescription>
            Help improve this project
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="rounded-lg border p-4">
              <h3 className="font-medium mb-2">Have Fun</h3>
              <p className="text-sm text-muted-foreground">
              Use this project for your own job search and get that offer!
              </p>
            </div>
            <div className="rounded-lg border p-4">
              <h3 className="font-medium mb-2">Report Issues</h3>
              <p className="text-sm text-muted-foreground">
                Found a bug or have a suggestion? Open an issue on GitHub or just ping me on LinkedIn!
              </p>
            </div>
            <div className="rounded-lg border p-4">
              <h3 className="font-medium mb-2">Share</h3>
              <p className="text-sm text-muted-foreground">
                Share it with others who might benefit from it.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="text-center">
        <h2 className="text-2xl font-bold mb-6 dark:text-white">
          Ready to Start?
        </h2>
        <div className="flex flex-col sm:flex-row justify-center gap-4">
          <Button
            className="bg-green-600 hover:bg-green-700 dark:bg-green-600 dark:hover:bg-green-500"
          >
            <Link 
                to="/" 
                className={storedTheme === 'dark' ? 'text-white' : ''}
            >
                Browse Jobs
            </Link>
          </Button>
          <Button
            variant="outline"
            onClick={() =>
              window.open("https://github.com/dy8r/applynow", "_blank")
            }
          >
            <GithubIcon className="mr-2 h-4 w-4" />
            Star on GitHub
          </Button>
          <Button
            variant="outline"
            onClick={() =>
              window.open("https://t.me/applynowalerts_bot", "_blank")
            }
          >
            Get Job Alerts
          </Button>
        </div>
      </div>
    </div>
  );
}
