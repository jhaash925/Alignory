import { useState } from "react";
import AnalysisCard from "../components/AnalysisCard";
import ATSDashboard from "../components/ATSDashboard";
import SiteHeader from "../components/SiteHeader";

const reviewStages = [
  {
    title: "Extracting resume text",
    detail: "Reading the uploaded file and pulling clean resume content."
  },
  {
    title: "Parsing resume sections",
    detail: "Identifying contact details, sections, bullets, dates, and skills."
  },
  {
    title: "Checking ATS readiness",
    detail: "Reviewing structure, formatting, readability, and keyword depth."
  },
  {
    title: "Scoring resume health",
    detail: "Calculating the general ATS score without using a job description."
  },
  {
    title: "Preparing your review",
    detail: "Building strengths, fix priorities, and recruiter-style guidance."
  }
];

const stageProgress = [18, 38, 58, 78, 92];

function ReviewOverlay({ stageIndex }) {
  const currentStage = reviewStages[Math.min(stageIndex, reviewStages.length - 1)];
  const progress = stageProgress[Math.min(stageIndex, stageProgress.length - 1)];

  return (
    <div className="fixed inset-0 z-50 flex min-h-screen items-center justify-center bg-[linear-gradient(180deg,rgba(255,251,235,0.88),rgba(240,249,255,0.92))] px-4 py-6">
      <div className="flex max-h-[88vh] w-full max-w-3xl flex-col overflow-hidden rounded-[32px] border border-white/85 bg-[rgba(255,255,255,0.95)] shadow-[0_24px_70px_rgba(15,23,42,0.16)] backdrop-blur">
        <div className="border-b border-slate-200/80 px-5 py-5 md:px-7">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <div className="text-xs font-semibold uppercase tracking-[0.24em] text-amber-700">
                General ATS Engine
              </div>
              <h2 className="mt-2 text-2xl font-bold text-slate-900 md:text-[2rem]">
                Reviewing your resume
              </h2>
              <p className="mt-2 max-w-xl text-sm leading-6 text-slate-600">
                {currentStage.detail}
              </p>
            </div>

            <div className="rounded-[22px] border border-amber-200 bg-amber-50 px-4 py-3 text-center">
              <div className="text-xs font-semibold uppercase tracking-[0.2em] text-amber-700">
                Progress
              </div>
              <div className="mt-1 text-3xl font-bold text-slate-900">
                {progress}%
              </div>
            </div>
          </div>

          <div className="mt-5 h-3 overflow-hidden rounded-full bg-slate-200">
            <div
              className="h-full rounded-full bg-[linear-gradient(90deg,#f59e0b,#38bdf8,#10b981)] transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        <div className="flex-1 overflow-y-auto px-5 py-4 md:px-7">
          <div className="space-y-3">
            {reviewStages.map((stage, index) => {
              const state =
                index < stageIndex ? "done" : index === stageIndex ? "active" : "pending";

              return (
                <div
                  key={stage.title}
                  className={`rounded-[22px] border px-4 py-4 transition md:px-5 ${
                    state === "done"
                      ? "border-emerald-200 bg-emerald-50/80"
                      : state === "active"
                        ? "border-amber-200 bg-amber-50/85"
                        : "border-slate-200 bg-slate-50/70"
                  }`}
                >
                  <div className="flex items-start gap-4">
                    <div
                      className={`mt-1 h-3.5 w-3.5 shrink-0 rounded-full ${
                        state === "done"
                          ? "bg-emerald-300"
                          : state === "active"
                            ? "bg-amber-300 animate-pulse"
                            : "bg-slate-500"
                      }`}
                    />

                    <div className="min-w-0">
                      <div className={`text-base font-semibold md:text-lg ${
                        state === "pending" ? "text-slate-500" : "text-slate-900"
                      }`}>
                        {stage.title}
                      </div>
                      <div className={`mt-1.5 text-sm leading-6 ${
                        state === "pending" ? "text-slate-500" : "text-slate-600"
                      }`}>
                        {stage.detail}
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

function GeneralReview() {
  const [resumeFile, setResumeFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingStage, setLoadingStage] = useState(0);

  const handleAnalyze = async () => {
    if (!resumeFile) {
      alert("Upload resume first");
      return;
    }

    setLoading(true);
    setLoadingStage(0);
    setResult(null);
    let backendStageInterval;

    try {
      const formData = new FormData();
      formData.append("file", resumeFile);

      const uploadResponse = await fetch("http://127.0.0.1:8000/upload-resume", {
        method: "POST",
        body: formData
      });

      if (!uploadResponse.ok) {
        const errorPayload = await uploadResponse.json().catch(() => ({}));
        throw new Error(errorPayload.detail || "Resume upload failed");
      }

      const uploadData = await uploadResponse.json();

      if (!uploadData.resume_text?.trim()) {
        throw new Error("No readable resume text was extracted");
      }

      setLoadingStage(1);

      backendStageInterval = window.setInterval(() => {
        setLoadingStage((current) => (current < 3 ? current + 1 : current));
      }, 1800);

      const response = await fetch("http://127.0.0.1:8000/general-ats-review", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          resume_text: uploadData.resume_text
        })
      });

      if (!response.ok) {
        const errorPayload = await response.json().catch(() => ({}));
        throw new Error(errorPayload.detail || "General ATS review failed");
      }

      window.clearInterval(backendStageInterval);
      setLoadingStage(4);

      const data = await response.json();
      await new Promise((resolve) => window.setTimeout(resolve, 350));
      setResult(data);
    } catch (error) {
      window.clearInterval(backendStageInterval);
      alert(error.message || "Error reviewing resume");
    }

    window.clearInterval(backendStageInterval);
    setLoading(false);
  };

  return (
    <div className="min-h-screen">
      <SiteHeader />

      <div className="mx-auto max-w-6xl px-4 py-8 md:px-8 md:py-10">
        <div className="overflow-hidden rounded-[32px] border border-white/70 bg-[rgba(255,255,255,0.82)] shadow-[0_24px_80px_rgba(15,23,42,0.1)] backdrop-blur">
          <div className="grid gap-8 px-6 py-8 md:grid-cols-[1.05fr_0.95fr] md:px-10 md:py-10">
            <div>
              <div className="inline-flex rounded-full border border-amber-200 bg-amber-50 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-amber-700">
                General ATS Review
              </div>

              <h1 className="mt-4 max-w-2xl text-4xl font-bold leading-tight text-slate-900 md:text-5xl">
                Score your resume without tying it to a specific job description.
              </h1>

              <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600 md:text-lg">
                Upload a resume and get a broad ATS health score focused on parser readiness, section quality, bullet strength, formatting, and recruiter clarity.
              </p>

              <div className="mt-8 grid gap-4 sm:grid-cols-3">
                <div className="rounded-2xl border border-amber-100 bg-amber-50/85 p-4">
                  <div className="text-xs font-semibold uppercase tracking-[0.18em] text-amber-700">
                    Structure
                  </div>
                  <div className="mt-2 text-2xl font-bold text-slate-900">
                    Sections
                  </div>
                </div>
                <div className="rounded-2xl border border-sky-100 bg-sky-50/85 p-4">
                  <div className="text-xs font-semibold uppercase tracking-[0.18em] text-sky-700">
                    Proof
                  </div>
                  <div className="mt-2 text-2xl font-bold text-slate-900">
                    Bullets
                  </div>
                </div>
                <div className="rounded-2xl border border-emerald-100 bg-emerald-50/85 p-4">
                  <div className="text-xs font-semibold uppercase tracking-[0.18em] text-emerald-700">
                    ATS Health
                  </div>
                  <div className="mt-2 text-2xl font-bold text-slate-900">
                    Readiness
                  </div>
                </div>
              </div>
            </div>

            <div className="rounded-[28px] border border-amber-100 bg-[linear-gradient(180deg,rgba(255,251,235,0.96),rgba(255,255,255,0.92))] p-6 shadow-[0_16px_40px_rgba(15,23,42,0.08)]">
              <label className="mb-2 block text-sm font-semibold uppercase tracking-[0.16em] text-slate-500">
                Resume Upload
              </label>

              <label className="flex cursor-pointer items-center justify-between gap-4 rounded-2xl border border-dashed border-slate-300 bg-white/80 px-4 py-4 transition hover:border-amber-400 hover:bg-amber-50/50">
                <div className="min-w-0">
                  <div className="truncate text-sm font-semibold text-slate-800">
                    {resumeFile ? resumeFile.name : "Choose PDF or DOCX"}
                  </div>
                  <div className="mt-1 text-sm text-slate-500">
                    The score uses only this resume.
                  </div>
                </div>

                <div className="shrink-0 rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white">
                  Browse
                </div>

                <input
                  type="file"
                  accept=".pdf,.docx"
                  className="hidden"
                  onChange={(e) => setResumeFile(e.target.files[0])}
                />
              </label>

              <button
                onClick={handleAnalyze}
                className="mt-5 inline-flex w-full items-center justify-center rounded-2xl bg-slate-900 px-6 py-4 text-sm font-semibold text-white transition hover:bg-amber-700"
              >
                {loading ? "Reviewing your resume..." : "Run General ATS Review"}
              </button>

              <div className="mt-5 grid gap-3">
                {[
                  "Contact and section parseability",
                  "ATS-safe formatting signals",
                  "Bullet clarity and measurable outcomes",
                  "Broad keyword and skills richness"
                ].map((item) => (
                  <div key={item} className="rounded-2xl border border-white/80 bg-white/80 px-4 py-4 text-sm text-slate-700">
                    {item}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {result && (
          <div className="mt-10">
            <ATSDashboard result={result} />

            <div className="mt-8">
              <AnalysisCard analysis={result.analysis} />
            </div>
          </div>
        )}
      </div>

      {loading && (
        <ReviewOverlay stageIndex={loadingStage} />
      )}
    </div>
  );
}

export default GeneralReview;
