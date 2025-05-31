import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import JobBoardLayout from "@/applynow/layouts/job-board-layout";
import JobDashboard from "@/applynow/pages/job-dashboard";
import JobDetail from "@/applynow/pages/job-detail";
import Resources from "./applynow/pages/resources";

export default function JobBoardPrototype() {
  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <JobBoardLayout>
              <JobDashboard />
            </JobBoardLayout>
          }
        />

        <Route
          path="/job/:id"
          element={
            <JobBoardLayout>
              <JobDetail />
            </JobBoardLayout>
          }
        />
        <Route
          path="/resources"
          element={
            <JobBoardLayout>
              <Resources />
            </JobBoardLayout>
          }
        />
      </Routes>
    </Router>
  );
}
