import { parseResumeDocument } from "./resumeSections";
import { SectionEntries } from "./templateHelpers";

// Tech template — dark gradient header, monospaced job titles, cyan accents
function TechTemplate({ resume, resumeData }) {
  const { header, sections } = parseResumeDocument(resumeData || resume);

  return (
    <div
      className="mx-auto max-w-[820px] overflow-hidden rounded-[16px] border border-slate-200 bg-white text-slate-900"
      style={{ fontFamily: "'Inter', 'Segoe UI', sans-serif" }}
    >
      {/* ── Dark header ── */}
      <header
        className="px-8 py-7"
        style={{ background: "linear-gradient(135deg, #0f172a 0%, #0f766e 100%)" }}
      >
        <div
          style={{
            fontSize: "1.85rem",
            fontWeight: 800,
            letterSpacing: "-0.03em",
            color: "#ffffff",
            lineHeight: 1.1,
            fontFamily: "'JetBrains Mono', 'Fira Code', 'Courier New', monospace",
          }}
        >
          {header.name}
        </div>

        {header.contact?.length > 0 && (
          <div className="mt-2.5 flex flex-wrap gap-x-4 text-[11px] text-cyan-200">
            {header.contact.map((item, i) => (
              <span key={i} className="flex items-center gap-1.5">
                {i > 0 && <span className="opacity-40">·</span>}
                {item}
              </span>
            ))}
          </div>
        )}

        {header.headline && (
          <p className="mt-3 max-w-3xl text-[12.5px] leading-[1.65] text-slate-300">
            {header.headline}
          </p>
        )}
      </header>

      {/* ── Body ── */}
      <div className="space-y-6 px-8 py-7 text-[12.5px] leading-[1.6]">
        {sections.map((section) => (
          <section key={section.title}>
            {/* Cyan pill label */}
            <div className="mb-3">
              <span className="inline-flex rounded-full bg-cyan-50 px-3.5 py-1 text-[9.5px] font-bold uppercase tracking-[0.25em] text-cyan-800 ring-1 ring-cyan-200">
                {section.title}
              </span>
            </div>

            <SectionEntries
              entries={section.entries}
              bulletDot="bg-cyan-600"
              accentColor="text-slate-900"
              dateColor="text-cyan-700"
              pillBg="bg-cyan-50"
              pillText="text-cyan-800"
              labelColor="text-cyan-700"
            />
          </section>
        ))}
      </div>
    </div>
  );
}

export default TechTemplate;
