import { Link } from "react-router-dom";
import SiteHeader from "../components/SiteHeader";

function ResumeBuilder() {
  return (
    <div className="min-h-screen">
      <SiteHeader />

      <div className="mx-auto max-w-6xl px-4 py-8 md:px-8 md:py-10">
        <div className="overflow-hidden rounded-[32px] border border-white/70 bg-[rgba(255,255,255,0.82)] shadow-[0_24px_80px_rgba(15,23,42,0.1)] backdrop-blur">
          <div className="grid gap-8 px-6 py-8 md:grid-cols-[1.05fr_0.95fr] md:px-10 md:py-10">
            <div>
              <div className="inline-flex rounded-full border border-sky-200 bg-sky-50 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-sky-700">
                Resume Builder
              </div>

              <h1 className="mt-4 max-w-2xl text-4xl font-bold leading-tight text-slate-900 md:text-5xl">
                Create polished resumes from structured sections instead of editing one long block.
              </h1>

              <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600 md:text-lg">
                This builder mode is where Alignory grows into a full resume platform with templates, section editing, export flows, and reusable profile data.
              </p>

              <div className="mt-8 grid gap-4 sm:grid-cols-3">
                <div className="rounded-2xl border border-sky-100 bg-sky-50/85 p-4">
                  <div className="text-xs font-semibold uppercase tracking-[0.18em] text-sky-700">
                    Structured
                  </div>
                  <div className="mt-2 text-sm leading-6 text-slate-700">
                    Edit resume sections cleanly instead of wrestling with one text blob
                  </div>
                </div>
                <div className="rounded-2xl border border-violet-100 bg-violet-50/85 p-4">
                  <div className="text-xs font-semibold uppercase tracking-[0.18em] text-violet-700">
                    Visual
                  </div>
                  <div className="mt-2 text-sm leading-6 text-slate-700">
                    Switch layouts and preview the result like a modern product
                  </div>
                </div>
                <div className="rounded-2xl border border-emerald-100 bg-emerald-50/85 p-4">
                  <div className="text-xs font-semibold uppercase tracking-[0.18em] text-emerald-700">
                    Exportable
                  </div>
                  <div className="mt-2 text-sm leading-6 text-slate-700">
                    Build resumes that are polished enough to ship immediately
                  </div>
                </div>
              </div>
            </div>

            <div className="rounded-[28px] border border-sky-100 bg-[linear-gradient(180deg,rgba(239,246,255,0.96),rgba(255,255,255,0.92))] p-6 shadow-[0_16px_40px_rgba(15,23,42,0.08)]">
              <div className="text-sm font-semibold uppercase tracking-[0.18em] text-sky-700">
                Builder Direction
              </div>

              <div className="mt-4 grid gap-3">
                {[
                  "Structured section editing",
                  "Template switching with live preview",
                  "ATS-friendly defaults",
                  "Stronger export-ready layouts",
                  "Reusable resume profiles for different roles"
                ].map((item) => (
                  <div key={item} className="rounded-2xl border border-white/80 bg-white/80 px-4 py-4 text-sm text-slate-700">
                    {item}
                  </div>
                ))}
              </div>

              <div className="mt-6 flex flex-wrap gap-3">
                <Link
                  to="/job-match"
                  className="inline-flex items-center rounded-2xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-teal-700"
                >
                  Open Current ATS Flow
                </Link>

                <Link
                  to="/improve-resume"
                  className="inline-flex items-center rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-800 transition hover:border-sky-300 hover:text-sky-700"
                >
                  View Template Studio
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResumeBuilder;
