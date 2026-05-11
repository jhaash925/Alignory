import { parseResumeDocument } from "./resumeSections";
import { ContactRow, SectionEntries } from "./templateHelpers";

function ModernTemplate({ resume, resumeData }) {
  const { header, sections } = parseResumeDocument(resumeData || resume);

  return (
    <div className="mx-auto max-w-[820px] border border-slate-300 bg-white px-10 py-10 text-slate-800" style={{ fontFamily: "'Inter', 'Segoe UI', sans-serif" }}>
      <header className="border-b border-slate-300 pb-5 text-center">
        <div style={{ fontSize: "1.95rem", fontWeight: 800, letterSpacing: "-0.02em", color: "#0f172a", lineHeight: 1.08 }}>
          {header.name}
        </div>

        <div className="mt-2 flex justify-center">
          <ContactRow contact={header.contact} tone="slate" />
        </div>

        {resumeData?.summary && (
          <p className="mx-auto mt-4 max-w-3xl text-left text-[12.2px] leading-[1.58] text-slate-700">
            {resumeData.summary}
          </p>
        )}
      </header>

      <div className="mt-6 space-y-6">
        {sections.map((section) => (
          <section key={section.title}>
            <div className="mb-3 flex items-center gap-3">
              <div className="rounded-full bg-slate-200 px-4 py-1 text-[10px] font-bold uppercase tracking-[0.18em] text-slate-700">
                {section.title}
              </div>
              <div className="h-px flex-1 bg-slate-300" />
            </div>

            <SectionEntries
              entries={section.entries}
              bulletDot="bg-slate-700"
              accentColor="text-slate-900"
              dateColor="text-slate-600"
              pillBg="bg-transparent"
              pillText="text-slate-700"
              labelColor="text-slate-900"
            />
          </section>
        ))}
      </div>
    </div>
  );
}

export default ModernTemplate;
