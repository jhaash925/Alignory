function getScoreTone(score) {

  if (score >= 78) {
    return {
      ring: "from-emerald-500 to-teal-500",
      text: "text-emerald-600",
      pill: "bg-emerald-50 text-emerald-700 border-emerald-200"
    };
  }

  if (score >= 60) {
    return {
      ring: "from-amber-400 to-orange-500",
      text: "text-amber-600",
      pill: "bg-amber-50 text-amber-700 border-amber-200"
    };
  }

  return {
    ring: "from-rose-500 to-red-500",
    text: "text-rose-600",
    pill: "bg-rose-50 text-rose-700 border-rose-200"
  };
}

function MetricCard({ label, value, note }) {

  return (
    <div className="rounded-[24px] border border-white/70 bg-white/90 p-5 shadow-[0_12px_32px_rgba(15,23,42,0.06)]">

      <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
        {label}
      </div>

      <div className="mt-2 text-3xl font-bold text-slate-900">
        {value}
      </div>

      <div className="mt-1.5 text-sm leading-6 text-slate-500">
        {note}
      </div>

    </div>
  );
}

function StatusIcon({ passed }) {

  return (
    <div className={`flex h-10 w-10 items-center justify-center rounded-full ${
      passed ? "bg-emerald-100 text-emerald-600" : "bg-rose-100 text-rose-600"
    }`}>
      <span className="text-xl font-bold">
        {passed ? "✓" : "×"}
      </span>
    </div>
  );
}

function getQualityCheckMessage(check) {

  const scoreText = typeof check.score === "number" ? ` Signal strength: ${check.score}%.` : "";

  if (check.passed) {
    return `We found ${check.label.toLowerCase()} in your resume, which helps it parse more cleanly in ATS systems.${scoreText}`;
  }

  return `Improve ${check.label.toLowerCase()} so the resume is easier for ATS systems and recruiters to interpret consistently.${scoreText}`;
}

function RequirementPanel({ title, items, tone, emptyText }) {

  const panelTone =
    tone === "positive"
      ? "border-emerald-200/80 bg-emerald-50/70"
      : "border-rose-200/80 bg-rose-50/70";

  const badgeTone =
    tone === "positive"
      ? "bg-emerald-100 text-emerald-700"
      : "bg-rose-100 text-rose-700";

  const proofTone = {
    strong: "bg-emerald-100 text-emerald-700",
    good: "bg-teal-100 text-teal-700",
    fair: "bg-amber-100 text-amber-700",
    weak: "bg-slate-200 text-slate-700",
    missing: "bg-rose-100 text-rose-700"
  };

  const recentTone = "bg-sky-100 text-sky-700";

  return (
    <div className={`rounded-[28px] border p-6 shadow-[0_16px_44px_rgba(15,23,42,0.06)] ${panelTone}`}>

      <h3 className="text-2xl font-semibold text-slate-900">
        {title}
      </h3>

      {items.length === 0 ? (
        <p className="mt-4 text-sm text-slate-500">
          {emptyText}
        </p>
      ) : (
        <div className="mt-5 space-y-3">

          {items.map((item, index) => (
            <div
              key={`${item.name}-${index}`}
              className="rounded-2xl border border-white/80 bg-white/90 p-4"
            >
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div className="text-lg font-semibold text-slate-900">
                  {item.name}
                </div>

                <div className="flex flex-wrap gap-2">
                  <span className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] ${badgeTone}`}>
                    {item.category.replace("_", " ")}
                  </span>

                  {item.proof_strength && item.proof_strength !== "missing" && (
                    <span className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] ${proofTone[item.proof_strength] || proofTone.fair}`}>
                      {item.proof_strength} proof
                    </span>
                  )}

                  {item.recent_evidence && (
                    <span className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] ${recentTone}`}>
                      recent
                    </span>
                  )}
                </div>
              </div>

              {item.sections?.length > 0 && (
                <p className="mt-2 text-sm text-slate-500">
                  Highlighted in {item.sections.join(", ")}
                </p>
              )}

              {item.evidence && (
                <p className="mt-3 text-sm leading-6 text-slate-700">
                  {item.evidence}
                </p>
              )}

            </div>
          ))}

        </div>
      )}

    </div>
  );
}

function EnterpriseDiagnostics({ profile, categorySummary }) {
  const diagnostics = profile?.diagnostics || {};
  const riskFlags = profile?.risk_flags || [];
  const categoryRows = Object.entries(categorySummary || {}).sort(
    ([left], [right]) => left.localeCompare(right)
  );

  return (
    <section className="rounded-[28px] border border-white/70 bg-white/90 p-6 shadow-[0_16px_44px_rgba(15,23,42,0.06)]">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h3 className="text-2xl font-semibold text-slate-900">
            Enterprise Parser Diagnostics
          </h3>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">
            This layer simulates the checks enterprise screening systems care about before a recruiter ever searches or filters the resume.
          </p>
        </div>

        <span className="rounded-full bg-slate-900 px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] text-white">
          Resume-only model
        </span>
      </div>

      <div className="mt-5 grid gap-4 md:grid-cols-3 xl:grid-cols-6">
        {[
          ["Parser", `${profile.parser_confidence ?? 0}%`],
          ["Search", `${profile.searchability_score ?? 0}%`],
          ["Evidence", `${profile.evidence_score ?? 0}%`],
          ["Timeline", `${profile.chronology_score ?? 0}%`],
          ["Metrics", diagnostics.metrics ?? 0],
          ["Risk Flags", riskFlags.length]
        ].map(([label, value]) => (
          <div key={label} className="rounded-2xl border border-slate-200 bg-slate-50/80 p-4">
            <div className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
              {label}
            </div>
            <div className="mt-2 text-2xl font-bold text-slate-900">
              {value}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 grid gap-5 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-2xl border border-slate-200 bg-slate-50/80 p-5">
          <h4 className="text-lg font-semibold text-slate-900">
            Signal Categories
          </h4>

          <div className="mt-4 space-y-3">
            {categoryRows.map(([category, summary]) => (
              <div key={category}>
                <div className="flex items-center justify-between gap-3 text-sm">
                  <span className="font-semibold text-slate-700">
                    {category}
                  </span>
                  <span className="text-slate-500">
                    {summary.score ?? 0}%
                  </span>
                </div>
                <div className="mt-2 h-2 overflow-hidden rounded-full bg-white">
                  <div
                    className="h-full rounded-full bg-[linear-gradient(90deg,#0f172a,#14b8a6)]"
                    style={{ width: `${summary.score ?? 0}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-slate-50/80 p-5">
          <h4 className="text-lg font-semibold text-slate-900">
            Risk Flags
          </h4>

          {riskFlags.length > 0 ? (
            <div className="mt-4 space-y-3">
              {riskFlags.slice(0, 5).map((flag) => (
                <div key={flag.label} className="rounded-xl bg-white px-4 py-3">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div className="text-sm font-semibold text-slate-900">
                      {flag.label}
                    </div>
                    <span className="rounded-full bg-rose-100 px-2.5 py-1 text-xs font-semibold uppercase tracking-[0.14em] text-rose-700">
                      {flag.severity}
                    </span>
                  </div>
                  <p className="mt-2 text-sm leading-6 text-slate-600">
                    {flag.message}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <p className="mt-4 text-sm leading-6 text-slate-600">
              No major enterprise ATS risk flags were detected.
            </p>
          )}
        </div>
      </div>
    </section>
  );
}

function ATSDashboard({ result }) {

  const breakdown = result.ats_breakdown;
  const isGeneralReview = result.mode === "general";
  const enterpriseProfile = breakdown?.enterprise_profile || result.enterprise_profile;
  const categorySummary = breakdown?.category_summary || {};
  const headlineScore = result.relevance_score ?? result.ats_score;
  const depthScore = result.ats_depth_score ?? result.ats_score;
  const matchedRequirements = breakdown?.matched_requirements || [];
  const missingRequirements = breakdown?.missing_requirements || [];
  const qualityChecks = breakdown?.quality_checks || [];
  const explanationCards = breakdown?.explanation_cards || [];
  const competencyCoverage = breakdown?.competency_coverage;
  const keywordHits = result.keyword_matched || [];
  const keywordMisses = result.keyword_missing || [];
  const passedChecks = qualityChecks.filter((check) => check.passed);
  const failedChecks = qualityChecks.filter((check) => !check.passed);
  const scoreTone = getScoreTone(headlineScore);
  const strengths = matchedRequirements.slice(0, 5);
  const priorities = missingRequirements.slice(0, 5);
  const scoreFactors = [
    {
      title: isGeneralReview ? "General ATS Score" : "Relevance Score",
      value: `${headlineScore}%`,
      description:
        isGeneralReview
          ? "This is the headline enterprise-style resume health score. It blends parser confidence, searchability, chronology, evidence, readability, and risk penalties without using a job description."
          : "This is the headline job-match score. It emphasizes hard skills, keyword overlap, and whether your resume looks aligned with the role at a glance.",
      factors: isGeneralReview
        ? [
            "Identity, contact, section taxonomy, and extraction confidence",
            "Skill searchability, role/title signals, and evidence-backed keywords",
            "Timeline quality, proof density, formatting risk, and professionalism"
          ]
        : [
            "Core technical or role-specific skills found in the resume",
            "Important job-description keywords matched",
            "Overall fit between the role and your listed capabilities"
          ]
    },
    {
      title: isGeneralReview ? "Resume Readiness" : "ATS Depth",
      value: `${depthScore}%`,
      description:
        isGeneralReview
          ? "This score reflects whether the resume can survive enterprise parsing and recruiter filtering before it is targeted to a specific role."
          : "This is the stricter score. It checks how strongly your resume proves the match, not just whether the right words appear.",
      factors: isGeneralReview
        ? [
            "Structured roles with company/title/date signals and timeline coverage",
            "Action-led bullets with distributed metrics and outcome language",
            "Low risk of tables, repeated headers, duplicate bullets, or generic filler"
          ]
        : [
            "Whether skills appear in Experience and Projects, not only in Skills",
            "Evidence strength, proof quality, and supporting role requirements",
            "Resume structure, ATS readiness, and deeper requirement coverage"
          ]
    }
  ];

  if (!isGeneralReview && competencyCoverage) {
    scoreFactors.push({
      title: "Competency Coverage",
      value: `${competencyCoverage.blended_score ?? 0}%`,
      description:
        "This set-based score compares the job's required competencies with the competencies detected in your resume. It helps balance semantic similarity with concrete requirement coverage.",
      factors: [
        `${competencyCoverage.intersection_count || 0} of ${competencyCoverage.required_count || 0} required competencies found`,
        `${competencyCoverage.required_only?.length || 0} required competencies still missing`,
        `${competencyCoverage.resume_only?.length || 0} extra resume competencies detected outside this job description`
      ]
    });
  }

  return (

    <div className="mt-8 space-y-8">

      <section className="overflow-hidden rounded-[32px] border border-white/70 bg-[rgba(255,255,255,0.82)] shadow-[0_22px_80px_rgba(15,23,42,0.1)] backdrop-blur">
        <div className="px-6 py-6 md:px-8 md:py-8">

          <div className="grid gap-4 xl:grid-cols-3">
            <div className="rounded-[28px] border border-white/70 bg-white/90 p-6 shadow-[0_12px_32px_rgba(15,23,42,0.06)] xl:col-span-2">
              <div className={`inline-flex rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] ${scoreTone.pill}`}>
                {isGeneralReview ? "General ATS Overview" : "ATS Match Overview"}
              </div>

              <div className="mt-5 flex flex-wrap items-end gap-4">
                <div className={`text-6xl font-bold ${scoreTone.text}`}>
                  {headlineScore}%
                </div>

                <div className="pb-2 text-sm text-slate-500">
                  {isGeneralReview ? "Resume health score" : "Relevance score for this role"}
                </div>
              </div>

              <div className="mt-5 h-3 overflow-hidden rounded-full bg-slate-200">
                <div
                  className={`h-full rounded-full bg-gradient-to-r ${scoreTone.ring}`}
                  style={{ width: `${headlineScore}%` }}
                />
              </div>

              <p className="mt-5 max-w-2xl text-sm leading-7 text-slate-600">
                {isGeneralReview
                  ? "This headline score reviews broad ATS readiness the way resume review tools do, without comparing against a specific job description."
                  : "This headline score emphasizes hard-skill overlap, keyword coverage, and core role fit, similar to commercial resume match tools."}
              </p>
            </div>

            <MetricCard
              label={isGeneralReview ? "Resume Readiness" : "ATS Depth"}
              value={`${depthScore}%`}
              note={isGeneralReview ? "Overall structure, content, readability, and parser readiness." : "Stricter evidence-based score including proof quality and supporting gaps."}
            />

            <MetricCard
              label={isGeneralReview ? "Strength Signals" : "Matched Skills"}
              value={matchedRequirements.length}
              note={isGeneralReview ? "Resume basics and quality signals already working." : "Role requirements your resume already supports."}
            />

            <MetricCard
              label={isGeneralReview ? "Fix Priorities" : "Missing Priorities"}
              value={missingRequirements.length}
              note={isGeneralReview ? "General ATS issues to improve first." : "Important gaps or weak signals to address."}
            />

            <MetricCard
              label={isGeneralReview ? "Detected Keywords" : "Keyword Coverage"}
              value={isGeneralReview ? keywordHits.length : `${keywordHits.length}/${result.important_keywords.length || 0}`}
              note={isGeneralReview ? "Skills and role terms detected in your resume." : "Important JD terms found in your resume."}
            />

          </div>

        </div>
      </section>

      <section className="rounded-[28px] border border-white/70 bg-white/90 p-6 shadow-[0_16px_44px_rgba(15,23,42,0.06)]">

        <h3 className="text-2xl font-semibold text-slate-900">
          How Scoring Works
        </h3>

        <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">
          {isGeneralReview
            ? "The dashboard reviews broad resume health, parser readiness, content depth, and proof quality without comparing against a specific job description."
            : "The dashboard shows two scores on purpose. One reflects broad job relevance, and the other checks how well your resume actually proves that match."}
        </p>

        <div className="mt-5 grid gap-4 xl:grid-cols-2">

          {scoreFactors.map((factor) => (
            <div
              key={factor.title}
              className="rounded-2xl border border-slate-200 bg-slate-50/80 p-5"
            >
              <div className="flex flex-wrap items-end justify-between gap-3">
                <div className="text-lg font-semibold text-slate-900">
                  {factor.title}
                </div>

                <div className="text-2xl font-bold text-slate-900">
                  {factor.value}
                </div>
              </div>

              <p className="mt-3 text-sm leading-6 text-slate-600">
                {factor.description}
              </p>

              <div className="mt-4 space-y-2">
                {factor.factors.map((item) => (
                  <div key={item} className="rounded-xl bg-white px-3 py-3 text-sm leading-6 text-slate-700">
                    {item}
                  </div>
                ))}
              </div>
            </div>
          ))}

        </div>

      </section>

      {isGeneralReview && enterpriseProfile && (
        <EnterpriseDiagnostics
          profile={enterpriseProfile}
          categorySummary={categorySummary}
        />
      )}

      <div className="grid gap-6">

        <RequirementPanel
          title="Strengths To Keep"
          items={strengths}
          tone="positive"
          emptyText="No clear strengths were detected yet."
        />

        <RequirementPanel
          title="Top Priorities To Fix"
          items={priorities}
          tone="negative"
          emptyText="No critical missing priorities detected."
        />

      </div>

      <div className="grid gap-6">

        <section className="rounded-[28px] border border-white/70 bg-white/90 p-6 shadow-[0_16px_44px_rgba(15,23,42,0.06)]">

          <div className="flex flex-wrap items-center gap-3">
            <h3 className="text-2xl font-semibold text-slate-900">
              ATS Readiness
            </h3>
            <span className="rounded-full bg-slate-800 px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] text-white">
              Important
            </span>
          </div>

          <p className="mt-2 text-sm leading-6 text-slate-500">
            These checks help your resume parse cleanly and look credible inside common applicant tracking systems.
          </p>

          <p className="mt-4 text-sm leading-6 text-slate-600">
            Tip: fix the red items first so recruiters and ATS systems can understand the structure of your resume more easily.
          </p>

          <div className="mt-6 overflow-hidden rounded-[24px] border border-slate-200">

            {qualityChecks.map((check) => (
              <div
                key={check.id}
                className="grid gap-4 border-b border-slate-200 bg-white px-5 py-5 md:grid-cols-[220px_56px_minmax(0,1fr)] md:items-start md:px-6"
              >
                <div className="text-lg font-semibold text-slate-800">
                  {check.label}
                </div>

                <div className="md:pt-0.5">
                  <StatusIcon passed={check.passed} />
                </div>

                <div className="min-w-0">
                  <div className={`text-sm font-semibold ${check.passed ? "text-emerald-700" : "text-rose-700"}`}>
                    {check.passed ? "Looks good" : "Needs improvement"}
                  </div>

                  <div className="mt-1 text-sm leading-7 text-slate-600">
                    {getQualityCheckMessage(check)}
                  </div>
                </div>
              </div>
            ))}

          </div>

        </section>

        <section className="rounded-[28px] border border-white/70 bg-white/90 p-6 shadow-[0_16px_44px_rgba(15,23,42,0.06)]">

          <h3 className="text-2xl font-semibold text-slate-900">
            Keyword Snapshot
          </h3>

          <p className="mt-2 text-sm leading-6 text-slate-500">
            Focus on the missing phrases first if you genuinely have that experience.
            {isGeneralReview ? " In general review mode, these are resume-quality signals rather than JD requirements." : ""}
          </p>

          <div className="mt-5">
            <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
              Found in resume
            </div>

            <div className="mt-3 flex flex-wrap gap-2">

              {keywordHits.length > 0 ? keywordHits.map((keyword, index) => (
                <span
                  key={`${keyword}-${index}`}
                  className="rounded-full bg-emerald-100 px-3 py-1 text-sm font-medium text-emerald-700"
                >
                  {keyword}
                </span>
              )) : (
                <span className="text-sm text-slate-500">
                  No strong keyword hits yet.
                </span>
              )}

            </div>
          </div>

          <div className="mt-6">
            <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
              Missing or weak
            </div>

            <div className="mt-3 flex flex-wrap gap-2">

              {keywordMisses.slice(0, 8).map((keyword, index) => (
                <span
                  key={`${keyword}-${index}`}
                  className="rounded-full bg-slate-200 px-3 py-1 text-sm font-medium text-slate-700"
                >
                  {keyword}
                </span>
              ))}

            </div>
          </div>

          <div className="mt-6 rounded-2xl bg-slate-50 p-4">
            <div className="text-sm font-semibold text-slate-900">
              Quick takeaway
            </div>

            <p className="mt-2 text-sm leading-6 text-slate-600">
              {isGeneralReview
                ? "Strong ATS resumes use standard sections, plain text contact details, action-led bullets, and measurable outcomes."
                : "Strong ATS resumes repeat the right skills in both the skills section and the experience bullets, not only once in a keyword list."}
            </p>
          </div>

        </section>

      </div>

      {explanationCards.length > 0 && (
        <section className="rounded-[28px] border border-white/70 bg-white/90 p-6 shadow-[0_16px_44px_rgba(15,23,42,0.06)]">

          <h3 className="text-2xl font-semibold text-slate-900">
            {isGeneralReview ? "Resume Health Insights" : "Match Insights"}
          </h3>

          <p className="mt-2 text-sm leading-6 text-slate-500">
            {isGeneralReview
              ? "These are the biggest score-shaping observations from the general ATS review."
              : "These are the biggest score-shaping observations from the current ATS analysis."}
          </p>

          <div className="mt-5 grid gap-4 md:grid-cols-2">

            {explanationCards.map((card, index) => (
              <div
                key={`${card.title}-${index}`}
                className={`rounded-2xl border p-4 ${
                  card.type === "missing"
                    ? "border-rose-200 bg-rose-50/70"
                    : "border-amber-200 bg-amber-50/70"
                }`}
              >
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div className="text-lg font-semibold text-slate-900">
                    {card.title}
                  </div>

                  <span className="rounded-full bg-white/80 px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] text-slate-700">
                    {card.severity}
                  </span>
                </div>

                <p className="mt-3 text-sm leading-6 text-slate-700">
                  {card.message}
                </p>
              </div>
            ))}

          </div>

        </section>
      )}

      {failedChecks.length > 0 && (
        <section className="rounded-[28px] border border-amber-200/80 bg-amber-50/80 p-6 shadow-[0_16px_44px_rgba(217,119,6,0.08)]">

          <h3 className="text-2xl font-semibold text-slate-900">
            Recommended Fixes
          </h3>

          <div className="mt-4 grid gap-3 md:grid-cols-2">

            {failedChecks.slice(0, 6).map((check) => (
              <div key={check.id} className="rounded-2xl bg-white/80 p-4 text-sm leading-6 text-slate-700">
                Add or improve <span className="font-semibold">{check.label.toLowerCase()}</span> so the resume reads more clearly in ATS parsing.
              </div>
            ))}

          </div>

        </section>
      )}

      {passedChecks.length > 0 && (
        <section className="rounded-[28px] border border-emerald-200/80 bg-emerald-50/70 p-6 shadow-[0_16px_44px_rgba(21,128,61,0.07)]">

          <h3 className="text-2xl font-semibold text-slate-900">
            What’s Already Working
          </h3>

          <div className="mt-4 flex flex-wrap gap-3">

            {passedChecks.slice(0, 8).map((check) => (
              <span
                key={check.id}
                className="rounded-full border border-emerald-200 bg-white/90 px-4 py-2 text-sm font-medium text-emerald-700"
              >
                {check.label}
              </span>
            ))}

          </div>

        </section>
      )}

    </div>

  );
}

export default ATSDashboard;
