import { parseResumeDocument } from "./resumeSections";
import { SectionEntries } from "./templateHelpers";

function MinimalTemplate({ resume, resumeData }) {
  const { header, sections } = parseResumeDocument(resumeData || resume);

  return (
    <div
      className="mx-auto max-w-[780px] bg-white text-slate-900"
      style={{ fontFamily: "'Inter', 'Helvetica Neue', sans-serif" }}
    >
      {/* ── Header — ultra-clean ── */}
      <header className="pb-6">
        <div
          style={{
            fontSize: "1.72rem",
            fontWeight: 600,
            letterSpacing: "-0.025em",
            color: "#0f172a",
            lineHeight: 1.1,
          }}
        >
          {header.name}
        </div>

        {header.contact?.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-x-4 text-[11px] text-slate-400">
            {header.contact.map((item, i) => (
              <span key={i}>{item}</span>
            ))}
          </div>
        )}

        {header.headline && (
          <p className="mt-3 max-w-2xl text-[12px] leading-[1.7] text-slate-500">
            {header.headline}
          </p>
        )}
      </header>

      {/* ── Sections ── */}
      <div className="space-y-6">
        {sections.map((section) => (
          <section key={section.title}>
            {/* Hairline + muted label */}
            <div className="mb-3 flex items-center gap-3">
              <div className="h-px flex-1 bg-slate-200" />
              <h2 className="text-[9px] font-bold uppercase tracking-[0.35em] text-slate-400">
                {section.title}
              </h2>
              <div className="h-px flex-1 bg-slate-200" />
            </div>

            <SectionEntries
              entries={section.entries}
              bulletDot="bg-slate-400"
              accentColor="text-slate-900"
              dateColor="text-slate-400"
              pillBg="bg-slate-50"
              pillText="text-slate-600"
              labelColor="text-slate-400"
            />
          </section>
        ))}
      </div>
    </div>
  );
}

export default MinimalTemplate;
