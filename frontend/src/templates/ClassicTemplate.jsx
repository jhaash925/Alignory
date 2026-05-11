import { parseResumeDocument } from "./resumeSections";
import { SectionEntries } from "./templateHelpers";

function ClassicTemplate({ resume, resumeData }) {
  const { header, sections } = parseResumeDocument(resumeData || resume);
  const summaryText = header.headline || resumeData?.summary || "";

  return (
    <div
      className="mx-auto max-w-[760px] bg-white px-4 py-3 text-slate-800 sm:px-6 sm:py-5"
      style={{ fontFamily: "'Georgia', 'Times New Roman', serif" }}
    >
      <header className="border-b-2 border-slate-700 pb-4 text-center">
        <div
          style={{
            fontSize: "2rem",
            fontWeight: 700,
            letterSpacing: "0.08em",
            color: "#111827",
            lineHeight: 1.15,
            fontFamily: "'Georgia', serif",
          }}
        >
          {header.name}
        </div>

        {header.contact?.length > 0 && (
          <div className="mt-2 flex flex-wrap items-center justify-center gap-x-3 gap-y-1 text-[11px] text-slate-700">
            {header.contact.map((item, i) => (
              <span key={i} className="flex items-center gap-2">
                {i > 0 && <span className="opacity-40">|</span>}
                {item}
              </span>
            ))}
          </div>
        )}

      </header>

      <div className="mt-5 space-y-5 text-[12px] leading-[1.6]">
        {summaryText && (
          <section>
            <div className="mb-2 flex items-center gap-3">
              <h2
                className="text-[10.5px] font-bold uppercase tracking-[0.22em] text-slate-900"
                style={{ fontFamily: "'Georgia', serif", letterSpacing: "0.2em" }}
              >
                Summary
              </h2>
              <div className="h-px flex-1 bg-slate-500" />
            </div>
            <p className="text-[12px] leading-[1.7] text-slate-800">
              {summaryText}
            </p>
          </section>
        )}

        {sections.map((section) => (
          <section key={section.title}>
            <div className="mb-2 flex items-center gap-3">
              <h2
                className="text-[10.5px] font-bold uppercase tracking-[0.22em] text-slate-900"
                style={{ fontFamily: "'Georgia', serif", letterSpacing: "0.2em" }}
              >
                {section.title}
              </h2>
              <div className="h-px flex-1 bg-slate-500" />
            </div>

            <div className="mt-3">
              <SectionEntries
                entries={section.entries}
                bulletDot="bg-slate-800"
                accentColor="text-slate-900"
                dateColor="text-slate-700"
                pillBg="bg-transparent"
                pillText="text-slate-800"
                labelColor="text-slate-900"
                skillsVariant="rows"
              />
            </div>
          </section>
        ))}
      </div>
    </div>
  );
}

export default ClassicTemplate;
