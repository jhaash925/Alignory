import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import HomePage from "./pages/HomePage";
import Dashboard from "./pages/Dashboard";
import GeneralReview from "./pages/GeneralReview";
import ImproveResume from "./pages/ImproveResume";
import ResumeBuilder from "./pages/ResumeBuilder";

function App() {

  return (

    <Router>

      <Routes>

        <Route
          path="/"
          element={<HomePage />}
        />

        <Route
          path="/job-match"
          element={<Dashboard />}
        />

        <Route
          path="/general-review"
          element={<GeneralReview />}
        />

        <Route
          path="/resume-builder"
          element={<ResumeBuilder />}
        />

        <Route
          path="/improve-resume"
          element={<ImproveResume />}
        />

      </Routes>

    </Router>

  );
}

export default App;
