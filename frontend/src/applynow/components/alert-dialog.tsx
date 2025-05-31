import React from "react";
import {
  AlertDialog as AlertDialogUI,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Button } from "@/components/ui/button";
import { BellIcon, CheckIcon } from "lucide-react";

interface AlertDialogProps {
  trigger?: React.ReactNode;
}

export default function AlertDialog({ trigger }: AlertDialogProps) {
  return (
    <AlertDialogUI>
      <AlertDialogTrigger asChild>
        {trigger || (
          <Button className="gap-2 bg-green-600 hover:bg-green-700 dark:bg-green-600 dark:hover:bg-green-500 text-white">
            <BellIcon className="h-4 w-4" />
            Get Alerts
          </Button>
        )}
      </AlertDialogTrigger>
      <AlertDialogContent className="sm:max-w-md">
        <AlertDialogHeader>
          <AlertDialogTitle>Get FREE Job Alerts on Telegram</AlertDialogTitle>
          <AlertDialogDescription>
            Receive instant notifications for new job postings that match your
            skills and preferences.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <div className="flex flex-col space-y-4 py-4">
          <div className="flex items-start space-x-4">
            <div className="mt-0.5 bg-green-100 dark:bg-green-900/30 p-1.5 rounded-full">
              <CheckIcon className="h-4 w-4 text-green-600 dark:text-green-500" />
            </div>
            <div>
              <h4 className="text-sm font-medium leading-none mb-1">
                Real-time notifications
              </h4>
              <p className="text-sm text-muted-foreground">
                Get notified as soon as relevant jobs are posted
              </p>
            </div>
          </div>
          <div className="flex items-start space-x-4">
            <div className="mt-0.5 bg-green-100 dark:bg-green-900/30 p-1.5 rounded-full">
              <CheckIcon className="h-4 w-4 text-green-600 dark:text-green-500" />
            </div>
            <div>
              <h4 className="text-sm font-medium leading-none mb-1">
                Personalized matches
              </h4>
              <p className="text-sm text-muted-foreground">
                Set your preferences and receive only relevant job postings
              </p>
            </div>
          </div>
          <div className="flex items-start space-x-4">
            <div className="mt-0.5 bg-green-100 dark:bg-green-900/30 p-1.5 rounded-full">
              <CheckIcon className="h-4 w-4 text-green-600 dark:text-green-500" />
            </div>
            <div>
              <h4 className="text-sm font-medium leading-none mb-1">
                Easy to use
              </h4>
              <p className="text-sm text-muted-foreground">
                No app installation required, works directly in Telegram
              </p>
            </div>
          </div>
        </div>
        <AlertDialogFooter className="flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2">
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction
            className="bg-green-600 hover:bg-green-700 dark:bg-green-600 dark:hover:bg-green-500 text-white"
            onClick={() =>
              window.open("https://t.me/applynowalerts_bot", "_blank")
            }
          >
            Join Telegram Channel
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialogUI>
  );
}
