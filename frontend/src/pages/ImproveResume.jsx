import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import TemplateSelector from "../components/TemplateSelector";
import SiteHeader from "../components/SiteHeader";

const resumeBuildStages = [
  {
    title: "Reading ATS recommendations",
    detail: "Pulling matched strengths, missing priorities, and rewrite direction from your latest analysis."
  },
  {
    title: "Rewriting your resume structure",
    detail: "Organizing the draft into cleaner ATS-friendly sections."
  },
  {
    title: "Preparing template preview",
    detail: "Getting the polished draft ready for template comparison and export."
  }
];

function ImproveResume() {

  const location = useLocation();
  const navigate = useNavigate();

  const result = location.state?.result;
  const jobDescription = location.state?.jobDescription;
  const resumeText = location.state?.resumeText;
  const [improvedResume, setImprovedResume] = useState(result?.improved_resume || "");
  const [improvedResumeData, setImprovedResumeData] = useState(result?.improved_resume_data || null);
  const [loadingDraft, setLoadingDraft] = useState(false);
  const [draftError, setDraftError] = useState("");
  const [draftStage, setDraftStage] = useState(0);
  const draftTimeoutMs = 60000;

  useEffect(() => {
    if (!loadingDraft) {
      setDraftStage(0);
      return undefined;
    }

    const interval = window.setInterval(() => {
      setDraftStage((current) => (
        current < resumeBuildStages.length - 1 ? current + 1 : current
      ));
    }, 1800);

    return () => window.clearInterval(interval);
  }, [loadingDraft]);

  useEffect(() => {
    if (!result || (improvedResume && improvedResumeData) || !jobDescription || !resumeText) {
      return undefined;
    }

    let cancelled = false;
    const controller = new AbortController();
    const timeoutId = window.setTimeout(() => {
      controller.abort();
    }, draftTimeoutMs);

    const buildResumeDraft = async () => {
      setLoadingDraft(true);
      setDraftStage(0);
      setDraftError("");

      try {
        const response = await fetch("http://127.0.0.1:8000/generate-improved-resume", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          signal: controller.signal,
          body: JSON.stringify({
            job_description: jobDescription,
            resume_text: resumeText
          })
        });

        if (!response.ok) {
          const errorPayload = await response.json().catch(() => ({}));
          throw new Error(errorPayload.detail || "Improved resume generation failed");
        }

        const data = await response.json();

        if (!cancelled) {
          setImprovedResume(data.improved_resume || "");
          setImprovedResumeData(data.improved_resume_data || null);
        }
      } catch (error) {
        if (!cancelled) {
          const message = error.name === "AbortError"
            ? "Improve Resume took too long to finish. Please try again in a few seconds. If it keeps happening, the local model may be busy."
            : (error.message || "Unable to build the improved resume");
          setDraftError(message);
        }
      } finally {
        window.clearTimeout(timeoutId);
        if (!cancelled) {
          setLoadingDraft(false);
        }
      }
    };

    buildResumeDraft();

    return () => {
      cancelled = true;
      window.clearTimeout(timeoutId);
      controller.abort();
    };
  }, [result, improvedResume, improvedResumeData, jobDescription, resumeText, draftTimeoutMs]);

  // Safety check if user refreshes page
  if (!result) {

    return (

      <div className="min-h-screen">
        <SiteHeader />

        <div className="mx-auto flex min-h-[70vh] max-w-2xl flex-col items-center justify-center px-6 py-10">
          <div className="rounded-[32px] border border-white/70 bg-[rgba(255,255,255,0.86)] p-10 text-center shadow-[0_24px_80px_rgba(15,23,42,0.1)] backdrop-blur">

            <h2 className="text-3xl font-semibold text-slate-900">
              No resume data found
            </h2>

            <p className="mt-3 max-w-md text-sm leading-6 text-slate-500">
              Open this page from the ATS dashboard after analyzing a resume so the tailored version can be previewed here.
            </p>

            <button
              onClick={() => navigate("/")}
              className="mt-6 inline-flex items-center rounded-2xl bg-slate-900 px-6 py-3 text-sm font-semibold text-white transition hover:bg-teal-700"
            >
              Go Back
            </button>
          </div>
        </div>
      </div>

    );
  }

  return (

    <div className="min-h-screen">
      <SiteHeader />

      <div className="mx-auto max-w-7xl px-4 py-8 md:px-8 md:py-10">

        <div className="mb-8 overflow-hidden rounded-[32px] border border-white/70 bg-[rgba(255,255,255,0.8)] shadow-[0_24px_80px_rgba(15,23,42,0.1)] backdrop-blur">
          <div className="grid gap-8 px-6 py-8 md:grid-cols-[1.15fr_0.85fr] md:px-10 md:py-10">

            <div>
              <div className="inline-flex rounded-full border border-teal-200 bg-teal-50 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-teal-700">
                Tailored Resume Studio
              </div>

              <h1 className="mt-4 max-w-2xl text-4xl font-bold leading-tight text-slate-900 md:text-5xl">
                Turn your ATS analysis into a polished resume draft.
              </h1>

              <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600 md:text-lg">
                Compare templates, preview the tailored version, and export a cleaner resume built from your latest ATS recommendations.
              </p>

              <div className="mt-8 grid gap-4 sm:grid-cols-3">
                <div className="rounded-2xl border border-teal-100 bg-teal-50/85 p-4 shadow-sm">
                  <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
                    Templates
                  </div>
                  <div className="mt-2 text-xl font-bold text-slate-900">
                    Switch fast
                  </div>
                </div>

                <div className="rounded-2xl border border-sky-100 bg-sky-50/85 p-4 shadow-sm">
                  <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
                    Preview
                  </div>
                  <div className="mt-2 text-xl font-bold text-slate-900">
                    Compare layouts
                  </div>
                </div>

                <div className="rounded-2xl border border-amber-100 bg-amber-50/85 p-4 shadow-sm">
                  <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
                    Export
                  </div>
                  <div className="mt-2 text-xl font-bold text-slate-900">
                    Cleaner final draft
                  </div>
                </div>
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-3 md:grid-cols-1">
              <div className="rounded-2xl border border-teal-100 bg-white/85 p-5 shadow-sm">
                <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
                  Relevance Score
                </div>
                <div className="mt-2 text-3xl font-bold text-slate-900">
                  {result.relevance_score ?? result.ats_score}%
                </div>
              </div>

              <div className="rounded-2xl border border-sky-100 bg-white/85 p-5 shadow-sm">
                <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
                  ATS Depth
                </div>
                <div className="mt-2 text-3xl font-bold text-slate-900">
                  {result.ats_depth_score ?? result.ats_score}%
                </div>
              </div>

              <div className="rounded-2xl border border-amber-100 bg-white/85 p-5 shadow-sm">
                <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
                  Matched Requirements
                </div>
                <div className="mt-2 text-3xl font-bold text-slate-900">
                  {result.matched_requirements?.length || 0}
                </div>
              </div>
            </div>
          </div>
        </div>

        {loadingDraft && (
          <div className="overflow-hidden rounded-[28px] border border-teal-100 bg-white/90 shadow-[0_16px_44px_rgba(15,23,42,0.06)]">
            <div className="border-b border-slate-200/80 px-6 py-6">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div>
                  <div className="text-xs font-semibold uppercase tracking-[0.22em] text-teal-700">
                    Tailored Resume In Progress
                  </div>
                  <h2 className="mt-2 text-3xl font-bold text-slate-900">
                    Building your polished draft
                  </h2>
                  <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600">
                    Your ATS report is ready. We’re now turning it into a cleaner resume draft for templates and export.
                  </p>
                </div>

                <div className="rounded-[22px] border border-teal-200 bg-teal-50 px-5 py-3 text-center">
                  <div className="text-xs font-semibold uppercase tracking-[0.18em] text-teal-700">
                    Progress
                  </div>
                  <div className="mt-1 text-3xl font-bold text-slate-900">
                    {draftStage === resumeBuildStages.length - 1 ? "92%" : `${36 + draftStage * 24}%`}
                  </div>
                </div>
              </div>

              <div className="mt-5 h-3 overflow-hidden rounded-full bg-slate-200">
                <div
                  className="h-full rounded-full bg-[linear-gradient(90deg,#14b8a6,#67e8f9,#c4b5fd)] transition-all duration-500"
                  style={{
                    width: draftStage === resumeBuildStages.length - 1 ? "92%" : `${36 + draftStage * 24}%`
                  }}
                />
              </div>
            </div>

            <div className="space-y-3 px-6 py-6">
              {resumeBuildStages.map((stage, index) => {
                const state =
                  index < draftStage ? "done" : index === draftStage ? "active" : "pending";

                return (
                  <div
                    key={stage.title}
                    className={`rounded-[22px] border px-5 py-4 ${
                      state === "done"
                        ? "border-emerald-200 bg-emerald-50/80"
                        : state === "active"
                          ? "border-cyan-200 bg-sky-50/80"
                          : "border-slate-200 bg-slate-50/80"
                    }`}
                  >
                    <div className="flex items-start gap-4">
                      <div
                        className={`mt-1 h-3.5 w-3.5 rounded-full ${
                          state === "done"
                            ? "bg-emerald-400"
                            : state === "active"
                              ? "bg-cyan-400 animate-pulse"
                              : "bg-slate-300"
                        }`}
                      />

                      <div>
                        <div className={`text-lg font-semibold ${
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
        )}

        {draftError && (
          <div className="rounded-[28px] border border-rose-200 bg-rose-50/80 p-6 text-sm text-rose-700 shadow-[0_16px_44px_rgba(15,23,42,0.06)]">
            {draftError}
          </div>
        )}

        {!loadingDraft && !draftError && (improvedResumeData || improvedResume) && (
          <TemplateSelector resume={improvedResume} resumeData={improvedResumeData} />
        )}

      </div>
    </div>

  );
}

export default ImproveResume;
