import { useState } from "react";
import { useNavigate } from "react-router-dom";
import AnalysisCard from "../components/AnalysisCard";
import ATSDashboard from "../components/ATSDashboard";
import SiteHeader from "../components/SiteHeader";

const analysisStages = [
  {
    title: "Extracting resume text",
    detail: "Reading the uploaded file and pulling clean resume content."
  },
  {
    title: "Parsing resume sections",
    detail: "Identifying skills, experience, projects, and education."
  },
  {
    title: "Matching against the job",
    detail: "Comparing keywords, role fit, and supporting evidence."
  },
  {
    title: "Scoring ATS signals",
    detail: "Calculating relevance, ATS depth, and missing priorities."
  },
  {
    title: "Preparing your review",
    detail: "Building the dashboard, insights, and tailored resume draft."
  }
];

const stageProgress = [18, 36, 54, 72, 88];

function AnalysisLoader({ stageIndex }) {
  const currentStage = analysisStages[Math.min(stageIndex, analysisStages.length - 1)];
  const progress = stageProgress[Math.min(stageIndex, stageProgress.length - 1)];

  return (
    <div className="mt-5 rounded-[24px] border border-slate-200/80 bg-slate-950 p-5 text-white shadow-[0_18px_42px_rgba(15,23,42,0.16)]">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <div className="text-xs font-semibold uppercase tracking-[0.2em] text-teal-200">
            ATS Analysis In Progress
          </div>
          <div className="mt-2 text-2xl font-bold text-white">
            {currentStage.title}
          </div>
        </div>

        <div className="rounded-full border border-teal-400/25 bg-teal-400/10 px-4 py-2 text-sm font-semibold text-teal-100">
          {progress}%
        </div>
      </div>

      <p className="mt-3 text-sm leading-7 text-slate-300">
        {currentStage.detail}
      </p>

      <div className="mt-5 h-2.5 overflow-hidden rounded-full bg-white/10">
        <div
          className="h-full rounded-full bg-[linear-gradient(90deg,#14b8a6,#67e8f9)] transition-all duration-500"
          style={{ width: `${progress}%` }}
        />
      </div>

      <div className="mt-5 grid gap-3">
        {analysisStages.map((stage, index) => {
          const state =
            index < stageIndex ? "done" : index === stageIndex ? "active" : "pending";

          return (
            <div
              key={stage.title}
              className={`flex items-start gap-3 rounded-2xl px-4 py-3 ${
                state === "done"
                  ? "bg-emerald-400/10"
                  : state === "active"
                    ? "bg-white/10"
                    : "bg-white/[0.04]"
              }`}
            >
              <div
                className={`mt-1 h-3 w-3 rounded-full ${
                  state === "done"
                    ? "bg-emerald-300"
                    : state === "active"
                      ? "bg-cyan-300 animate-pulse"
                      : "bg-slate-500"
                }`}
              />

              <div>
                <div className={`text-sm font-semibold ${
                  state === "pending" ? "text-slate-400" : "text-white"
                }`}>
                  {stage.title}
                </div>

                <div className={`mt-1 text-sm leading-6 ${
                  state === "pending" ? "text-slate-500" : "text-slate-300"
                }`}>
                  {stage.detail}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function FullPageAnalysisOverlay({ stageIndex }) {
  const currentStage = analysisStages[Math.min(stageIndex, analysisStages.length - 1)];
  const progress = stageProgress[Math.min(stageIndex, stageProgress.length - 1)];

  return (
    <div className="fixed inset-0 z-50 flex min-h-screen items-center justify-center bg-[radial-gradient(circle_at_top,rgba(45,212,191,0.12),transparent_28%),linear-gradient(180deg,rgba(248,252,252,0.82)_0%,rgba(240,249,255,0.88)_100%)] px-4 py-6">
      <div className="flex max-h-[88vh] w-full max-w-3xl flex-col overflow-hidden rounded-[32px] border border-white/85 bg-[rgba(255,255,255,0.94)] shadow-[0_24px_70px_rgba(15,23,42,0.16)] backdrop-blur">
        <div className="border-b border-slate-200/80 px-5 py-5 md:px-7 md:py-5">
          <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="text-xs font-semibold uppercase tracking-[0.24em] text-teal-700">
              Alignory Analysis Engine
            </div>
            <h2 className="mt-2 text-2xl font-bold text-slate-900 md:text-[2rem]">
              Analyzing your resume
            </h2>
            <p className="mt-2 max-w-xl text-sm leading-6 text-slate-600">
              Parsing the resume, matching it to the role, and preparing your ATS review.
            </p>
          </div>

          <div className="rounded-[22px] border border-teal-200 bg-teal-50 px-4 py-3 text-center">
            <div className="text-xs font-semibold uppercase tracking-[0.2em] text-teal-700">
              Progress
            </div>
            <div className="mt-1 text-3xl font-bold text-slate-900">
              {progress}%
            </div>
          </div>
        </div>

        <div className="mt-5 h-3 overflow-hidden rounded-full bg-slate-200">
          <div
            className="h-full rounded-full bg-[linear-gradient(90deg,#14b8a6,#67e8f9,#c4b5fd)] transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
        </div>

        <div className="flex-1 overflow-y-auto px-5 py-4 md:px-7">
        <div className="space-y-3">
          {analysisStages.map((stage, index) => {
            const state =
              index < stageIndex ? "done" : index === stageIndex ? "active" : "pending";

            return (
              <div
                key={stage.title}
                className={`rounded-[22px] border px-4 py-4 transition md:px-5 ${
                state === "done"
                  ? "border-emerald-200 bg-emerald-50/80"
                  : state === "active"
                      ? "border-cyan-200 bg-sky-50/85"
                      : "border-slate-200 bg-slate-50/70"
              }`}
              >                
                <div className="flex items-start gap-4">
                  <div
                    className={`mt-1 h-3.5 w-3.5 shrink-0 rounded-full ${
                      state === "done"
                        ? "bg-emerald-300"
                        : state === "active"
                          ? "bg-cyan-300 animate-pulse"
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

        <div className="mt-4 rounded-[20px] border border-slate-200 bg-slate-50/80 px-4 py-3 text-sm leading-6 text-slate-600">
          Current step: <span className="font-semibold text-slate-900">{currentStage.title}</span>
        </div>
        </div>
      </div>
    </div>
  );
}

function Dashboard() {

  const navigate = useNavigate();

  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingStage, setLoadingStage] = useState(0);
  const [lastResumeText, setLastResumeText] = useState("");
  const [extractionInfo, setExtractionInfo] = useState(null);

  const handleAnalyze = async () => {

    if (!resumeFile) {
      alert("Upload resume first");
      return;
    }

    if (!jobDescription) {
      alert("Enter job description");
      return;
    }

    setLoading(true);
    setLoadingStage(0);
    setResult(null);
    setExtractionInfo(null);
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

      setLastResumeText(uploadData.resume_text);
      setExtractionInfo(uploadData.extraction || null);
      setLoadingStage(1);

      backendStageInterval = window.setInterval(() => {
        setLoadingStage((current) => (current < 3 ? current + 1 : current));
      }, 2200);

      const response = await fetch(
        "http://127.0.0.1:8000/generate-resume",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            job_description: jobDescription,
            resume_text: uploadData.resume_text
          })
        }
      );

      if (!response.ok) {
        const errorPayload = await response.json().catch(() => ({}));
        throw new Error(errorPayload.detail || "ATS analysis failed");
      }

      window.clearInterval(backendStageInterval);
      setLoadingStage(4);

      const data = await response.json();
      await new Promise((resolve) => window.setTimeout(resolve, 350));

      setResult({
        ...data,
        extraction: uploadData.extraction
      });

    } catch (error) {
      window.clearInterval(backendStageInterval);

      alert(error.message || "Error analyzing resume");

    }

    window.clearInterval(backendStageInterval);
    setLoading(false);
  };


  return (

    <div className="min-h-screen">
      <SiteHeader />

      <div className="mx-auto w-full max-w-6xl px-4 py-8 md:px-8 md:py-10">

        <div className="mb-8 overflow-hidden rounded-[32px] border border-white/60 bg-[rgba(255,255,255,0.78)] shadow-[0_24px_80px_rgba(16,35,28,0.12)] backdrop-blur">

          <div className="grid gap-8 px-6 py-8 md:grid-cols-[1.15fr_0.85fr] md:px-10 md:py-10">

            <div>
              <div className="mb-4 inline-flex items-center rounded-full border border-teal-200 bg-teal-50 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-teal-700">
                Alignory Job Match
              </div>

              <h1 className="max-w-2xl text-4xl font-bold leading-tight text-slate-900 md:text-5xl">
                Target your resume to a real job description and see exactly how it performs.
              </h1>

              <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600 md:text-lg">
                Upload your resume, paste the job description, and get a polished recruiter-style view of strengths,
                missing priorities, and ATS readiness.
              </p>

              <div className="mt-8 grid gap-4 sm:grid-cols-3">
                <div className="rounded-2xl border border-teal-100 bg-teal-50/85 p-4 shadow-sm">
                  <div className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                    Match Review
                  </div>
                  <div className="mt-2 text-2xl font-bold text-slate-900">
                    Skills + fit
                  </div>
                </div>

                <div className="rounded-2xl border border-sky-100 bg-sky-50/85 p-4 shadow-sm">
                  <div className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                    ATS Readiness
                  </div>
                  <div className="mt-2 text-2xl font-bold text-slate-900">
                    Structure + proof
                  </div>
                </div>

                <div className="rounded-2xl border border-amber-100 bg-amber-50/85 p-4 shadow-sm">
                  <div className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                    Resume Rewrite
                  </div>
                  <div className="mt-2 text-2xl font-bold text-slate-900">
                    Tailored output
                  </div>
                </div>
              </div>
            </div>

            <div className="rounded-[28px] border border-teal-100/80 bg-[linear-gradient(180deg,rgba(255,255,255,0.96),rgba(240,253,250,0.9))] p-6 shadow-[0_16px_40px_rgba(15,23,42,0.08)]">

              <div className="mb-5">
                <label className="mb-2 block text-sm font-semibold uppercase tracking-[0.16em] text-slate-500">
                  Resume Upload
                </label>

                <label className="flex cursor-pointer items-center justify-between rounded-2xl border border-dashed border-slate-300 bg-slate-50/80 px-4 py-4 transition hover:border-teal-400 hover:bg-teal-50/50">
                  <div>
                    <div className="text-sm font-semibold text-slate-800">
                      {resumeFile ? resumeFile.name : "Choose PDF or DOCX"}
                    </div>
                    <div className="mt-1 text-sm text-slate-500">
                      Best results come from clear headings and readable text.
                    </div>
                  </div>

                  <div className="rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white">
                    Browse
                  </div>

                  <input
                    type="file"
                    accept=".pdf,.docx"
                    className="hidden"
                    onChange={(e) =>
                      {
                        setResumeFile(e.target.files[0]);
                        setExtractionInfo(null);
                      }
                    }
                  />
                </label>

                {extractionInfo && (
                  <div className="mt-3 rounded-2xl border border-slate-200 bg-white/80 px-4 py-3 text-sm leading-6 text-slate-600">
                    Extracted {extractionInfo.text_words || 0} words using {extractionInfo.method === "ocr_fallback" ? "OCR fallback" : "direct text parsing"}.
                    {extractionInfo.method === "ocr_fallback" && ` OCR was used on ${extractionInfo.pages_with_ocr || 0} page${extractionInfo.pages_with_ocr === 1 ? "" : "s"}.`}
                  </div>
                )}
              </div>

              <div>
                <label className="mb-2 block text-sm font-semibold uppercase tracking-[0.16em] text-slate-500">
                  Job Description
                </label>

                <textarea
                  className="min-h-[220px] w-full rounded-2xl border border-slate-200 bg-white px-4 py-4 text-sm leading-6 text-slate-700 shadow-inner outline-none transition focus:border-teal-500 focus:ring-4 focus:ring-teal-100"
                  rows="8"
                  placeholder="Paste the full job description here..."
                  value={jobDescription}
                  onChange={(e) =>
                    setJobDescription(e.target.value)
                  }
                />
              </div>

              <button
                onClick={handleAnalyze}
                className="mt-5 inline-flex w-full items-center justify-center rounded-2xl bg-slate-900 px-6 py-4 text-sm font-semibold text-white transition hover:bg-teal-700"
              >
                {loading ? "Analyzing your resume..." : "Run ATS Analysis"}
              </button>

            </div>
          </div>
        </div>

        {result && (

          <div className="mt-10">

            <ATSDashboard result={result} />

            <div className="mt-8">
              <AnalysisCard analysis={result.analysis} />
            </div>

            <button
              onClick={() =>
                navigate("/improve-resume", {
                  state: {
                    result,
                    jobDescription,
                    resumeText: lastResumeText
                  }
                })
              }
              className="mt-8 inline-flex items-center rounded-2xl bg-teal-700 px-6 py-3 text-sm font-semibold text-white transition hover:bg-teal-800"
            >
              Improve Resume
            </button>

          </div>

        )}

      </div>

      {loading && (
        <FullPageAnalysisOverlay stageIndex={loadingStage} />
      )}
    </div>
  );
}

export default Dashboard;
