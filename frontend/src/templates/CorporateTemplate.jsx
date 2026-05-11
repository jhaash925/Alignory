import { parseResumeDocument } from "./resumeSections";
import { SectionEntries } from "./templateHelpers";

// Corporate template — formal two-column header, structured typography, navy accents
function CorporateTemplate({ resume, resumeData }) {
  const { header, sections } = parseResumeDocument(resumeData || resume);
  const summaryText = resumeData?.summary || header.headline || "";

  return (
    <div
      className="mx-auto max-w-[820px] bg-white text-slate-800"
      style={{ fontFamily: "'Inter', 'Segoe UI', sans-serif" }}
    >
      <div className="h-2 w-full" style={{ background: "#1e3a5f" }} />

      <header className="border-b border-slate-300 px-8 py-6">
        <div className="space-y-2">
          <div
            className="md:whitespace-nowrap"
            style={{
              fontSize: "2.35rem",
              fontWeight: 700,
              letterSpacing: "0.01em",
              color: "#1e3a5f",
              lineHeight: 1,
            }}
          >
            {header.name}
          </div>

          {header.contact?.length > 0 && (
            <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-[11.5px] leading-[1.5] text-slate-600">
              {header.contact.map((item, i) => (
                <span key={i} className="flex items-center gap-2">
                  {i > 0 && <span className="opacity-40">|</span>}
                  {item}
                </span>
              ))}
            </div>
          )}

          {summaryText && (
            <p className="max-w-none pt-1 text-[12.2px] leading-[1.6] text-slate-600">
              {summaryText}
            </p>
          )}
        </div>
      </header>

      <div className="space-y-5 px-8 py-6 text-[12.25px] leading-[1.6]">
        {sections.map((section) => (
          <section key={section.title}>
            <div className="mb-3 flex items-center gap-3">
              <div className="h-4 w-[3px] rounded-full" style={{ background: "#1e3a5f" }} />
              <h2
                className="text-[10px] font-bold uppercase tracking-[0.26em]"
                style={{ color: "#1e3a5f" }}
              >
                {section.title}
              </h2>
              <div className="h-px flex-1 bg-slate-200" />
            </div>

            <SectionEntries
              entries={section.entries}
              bulletDot="bg-[#1e3a5f]"
              accentColor="text-slate-900"
              dateColor="text-slate-600"
              pillBg="bg-transparent"
              pillText="text-slate-700"
              labelColor="text-[#1e3a5f]"
              skillsVariant="rows"
            />
          </section>
        ))}
      </div>
      <div className="h-1 w-full" style={{ background: "#1e3a5f", opacity: 0.3 }} />
    </div>
  );
}

export default CorporateTemplate;
