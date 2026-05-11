import { Link } from "react-router-dom";
import SiteHeader from "../components/SiteHeader";

const products = [
  {
    title: "Job Match Review",
    path: "/job-match",
    eyebrow: "Targeted ATS",
    description:
      "Score your resume against a real job description with relevance, ATS depth, missing priorities, and rewrite direction.",
    tone: "border-teal-200 bg-[linear-gradient(180deg,rgba(240,253,250,0.95),rgba(255,255,255,0.9))]"
  },
  {
    title: "General ATS Review",
    path: "/general-review",
    eyebrow: "Resume Health",
    description:
      "Review structure, bullet quality, readability, formatting, and overall ATS readiness without a specific JD.",
    tone: "border-sky-200 bg-[linear-gradient(180deg,rgba(239,246,255,0.95),rgba(255,255,255,0.9))]"
  },
  {
    title: "Resume Builder",
    path: "/resume-builder",
    eyebrow: "Builder Studio",
    description:
      "Create cleaner resumes through structured sections, polished templates, and export-ready presentation.",
    tone: "border-amber-200 bg-[linear-gradient(180deg,rgba(255,251,235,0.95),rgba(255,255,255,0.9))]"
  }
];

const benefits = [
  {
    title: "Role Fit With Context",
    description: "See whether your resume looks right for the role, not just whether a few skills happen to overlap."
  },
  {
    title: "ATS Detail That Matters",
    description: "Understand proof strength, section quality, and the gaps that actually affect how credible your resume feels."
  },
  {
    title: "Builder + Review In One Place",
    description: "Move from analysis to improvement without switching products or losing the context of what the job needs."
  }
];

function ProductMock() {
  return (
    <div className="relative self-start overflow-hidden rounded-[32px] border border-slate-200/80 bg-slate-950 p-5 shadow-[0_24px_70px_rgba(15,23,42,0.22)]">
      <div className="absolute inset-x-0 top-0 h-32 bg-[radial-gradient(circle_at_top,rgba(45,212,191,0.24),transparent_60%)]" />

      <div className="relative rounded-[24px] border border-white/10 bg-white/5 p-4">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-[11px] font-semibold uppercase tracking-[0.2em] text-teal-200/90">
              Example Review
            </div>
            <div className="mt-2 text-2xl font-bold text-white">
              Resume Match
            </div>
          </div>

          <div className="rounded-full border border-teal-400/30 bg-teal-400/15 px-4 py-2 text-sm font-semibold text-teal-100">
            91% Relevance
          </div>
        </div>

        <div className="mt-5 grid gap-3 md:grid-cols-[1.05fr_0.95fr]">
          <div className="rounded-2xl bg-white px-4 py-4">
            <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
              Strengths
            </div>
            <div className="mt-4 space-y-2">
              {["React", "TypeScript", "Machine Learning", "Python"].map((item) => (
                <div key={item} className="rounded-xl bg-emerald-50 px-3 py-3 text-sm font-semibold text-emerald-800">
                  {item}
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-3">
            <div className="rounded-2xl border border-white/10 bg-white/8 px-4 py-4">
              <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-300">
                ATS Depth
              </div>
              <div className="mt-2 text-3xl font-bold text-white">
                86%
              </div>
              <div className="mt-2 text-sm leading-6 text-slate-300">
                Evidence-aware score that looks at section quality, proof strength, and missing supporting signals.
              </div>
            </div>

            <div className="rounded-2xl border border-white/10 bg-white/8 px-4 py-4">
              <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-300">
                Missing Priorities
              </div>
              <div className="mt-3 flex flex-wrap gap-2">
                {["MLOps", "System Design", "Deployment"].map((item) => (
                  <span key={item} className="rounded-full bg-white/10 px-3 py-1 text-sm text-slate-100">
                    {item}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function HomePage() {
  return (
    <div className="min-h-screen">
      <SiteHeader />

      <div className="mx-auto max-w-7xl px-4 py-6 md:px-8 md:py-8">
        <section className="overflow-hidden rounded-[36px] border border-white/70 bg-[rgba(255,255,255,0.82)] shadow-[0_24px_90px_rgba(15,23,42,0.12)] backdrop-blur">
          <div className="grid items-start gap-10 px-6 py-8 lg:grid-cols-[1.02fr_0.98fr] lg:px-10 lg:py-12">
            <div>
              <div className="inline-flex items-center rounded-full border border-teal-200 bg-teal-50 px-3 py-1 text-xs font-semibold uppercase tracking-[0.22em] text-teal-700">
                Alignory Platform
              </div>

              <h1 className="mt-5 max-w-3xl text-5xl font-bold leading-[1.02] text-slate-900 md:text-6xl xl:text-7xl">
                Build sharper resumes and understand exactly how they perform.
              </h1>

              <p className="mt-5 max-w-2xl text-base leading-8 text-slate-600 md:text-lg">
                Alignory combines job match analysis, ATS review, and resume building in one workspace designed for people who want both clarity and polish.
              </p>
            </div>

            <ProductMock />
          </div>

          <div className="grid gap-4 border-t border-slate-100/80 px-6 pb-8 pt-2 sm:grid-cols-2 lg:px-10 lg:pb-10">
            <div className="rounded-[28px] border border-orange-100 bg-[linear-gradient(180deg,rgba(255,251,235,0.96),rgba(255,255,255,0.9))] p-6 shadow-[0_12px_36px_rgba(15,23,42,0.06)]">
              <div className="text-xs font-semibold uppercase tracking-[0.2em] text-amber-700">
                Designed For
              </div>
              <div className="mt-3 text-2xl font-bold text-slate-900">
                Job seekers who want both clarity and polish
              </div>
              <p className="mt-3 max-w-xl text-sm leading-7 text-slate-600">
                Use one product for targeted JD matching, general ATS review, and resume creation instead of juggling separate tools.
              </p>
            </div>

            <div className="rounded-[28px] border border-sky-100 bg-[linear-gradient(180deg,rgba(240,249,255,0.96),rgba(255,255,255,0.9))] p-6 shadow-[0_12px_36px_rgba(15,23,42,0.08)]">
              <div className="text-xs font-semibold uppercase tracking-[0.2em] text-sky-700">
                Core Modes
              </div>
              <div className="mt-4 rounded-2xl border border-sky-200/80 bg-sky-100/70 px-5 py-4">
                <div className="space-y-3 text-base leading-7 text-slate-800">
                  <div>Targeted ATS matching for a specific role</div>
                  <div className="h-px bg-sky-200/80" />
                  <div>General ATS health without a JD</div>
                  <div className="h-px bg-sky-200/80" />
                  <div>Resume building and export-ready templates</div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="mt-8 grid gap-6 xl:grid-cols-3">
          {products.map((product) => (
            <Link
              key={product.title}
              to={product.path}
              className={`group flex min-h-[300px] flex-col overflow-hidden rounded-[30px] border p-6 shadow-[0_18px_48px_rgba(15,23,42,0.08)] transition hover:-translate-y-1 hover:shadow-[0_24px_54px_rgba(15,23,42,0.12)] ${product.tone}`}
            >
              <div className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                {product.eyebrow}
              </div>

              <h2 className="mt-4 min-h-[76px] text-3xl font-bold leading-tight text-slate-900">
                {product.title}
              </h2>

              <p className="mt-4 min-h-[112px] text-sm leading-7 text-slate-600">
                {product.description}
              </p>

              <div className="mt-auto inline-flex items-center pt-8 text-sm font-semibold text-slate-900 transition group-hover:text-teal-700">
                Open workspace
              </div>
            </Link>
          ))}
        </section>

        <section className="mt-8 rounded-[34px] border border-white/70 bg-[rgba(255,255,255,0.82)] px-6 py-8 shadow-[0_18px_54px_rgba(15,23,42,0.08)] backdrop-blur md:px-8">
          <div className="max-w-3xl">
            <div className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
              Why Alignory
            </div>
            <h2 className="mt-4 text-4xl font-bold text-slate-900">
              A sharper workflow from analysis to improvement
            </h2>
            <p className="mt-4 text-base leading-8 text-slate-600">
              The product is designed to help you move from “what is wrong with my resume?” to “how do I improve it?” without breaking context.
            </p>
          </div>

          <div className="mt-8 grid gap-5 lg:grid-cols-3">
            {benefits.map((benefit) => (
              <div key={benefit.title} className="flex min-h-[320px] flex-col rounded-[26px] border border-slate-100 bg-white/85 p-6 shadow-[0_10px_24px_rgba(15,23,42,0.05)]">
                <div className="h-10 w-10 rounded-2xl bg-[linear-gradient(180deg,rgba(15,23,42,0.9),rgba(15,118,110,0.85))]" />
                <h3 className="mt-5 min-h-[104px] text-2xl font-bold leading-tight text-slate-900">
                  {benefit.title}
                </h3>
                <p className="mt-3 text-sm leading-7 text-slate-600">
                  {benefit.description}
                </p>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

export default HomePage;
