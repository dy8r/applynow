// useAnalytics.ts
import { useEffect } from "react"
import { sendAnalytics } from "@/applynow/data/job-postings-data"

export function useAnalytics(path?: string) {
  useEffect(() => {
    sendAnalytics(path).then(() => {
    }).catch(err => {
      // Optional: log or ignore
      console.warn("Analytics failed:", err)
    })
  }, [path])
}
