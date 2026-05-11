import { useState } from "react";
import ModernTemplate from "../templates/ModernTemplate";
import ClassicTemplate from "../templates/ClassicTemplate";
import MinimalTemplate from "../templates/MinimalTemplate";
import TechTemplate from "../templates/TechTemplate";
import CorporateTemplate from "../templates/CorporateTemplate";
import html2pdf from "html2pdf.js";

function TemplateSelector({ resume, resumeData }) {

const [template, setTemplate] = useState("classic");

const templates = [
  {
    id: "modern",
    name: "Modern",
    description: "Bold, clean, and balanced for product or frontend roles."
  },
  {
    id: "classic",
    name: "Classic",
    description: "Traditional and recruiter-friendly for formal applications."
  },
  {
    id: "minimal",
    name: "Minimal",
    description: "Simple and quiet layout with very low visual noise."
  },
  {
    id: "tech",
    name: "Tech",
    description: "Sharper styling for engineering-heavy resumes and projects."
  },
  {
    id: "corporate",
    name: "Corporate",
    description: "Structured presentation for business-facing or enterprise roles."
  }
];

const downloadPDF = () => {


const element = document.getElementById("resume-preview");

const options = {
  margin: 0.5,
  filename: "resume.pdf",
  image: { type: "jpeg", quality: 0.98 },
  html2canvas: { scale: 2 },
  jsPDF: { unit: "in", format: "letter", orientation: "portrait" }
};

html2pdf().set(options).from(element).save();


};

const renderTemplate = () => {


switch(template) {

  case "classic":
    return <ClassicTemplate resume={resume} resumeData={resumeData} />;

  case "minimal":
    return <MinimalTemplate resume={resume} resumeData={resumeData} />;

  case "tech":
    return <TechTemplate resume={resume} resumeData={resumeData} />;

  case "corporate":
    return <CorporateTemplate resume={resume} resumeData={resumeData} />;

  default:
    return <ModernTemplate resume={resume} resumeData={resumeData} />;
}


};

return (


<div className="grid gap-6 xl:grid-cols-[340px_1fr]">

  {/* LEFT PANEL — TEMPLATE SELECTION */}

  <div className="rounded-[28px] border border-white/70 bg-[rgba(255,255,255,0.88)] p-6 shadow-[0_16px_44px_rgba(15,23,42,0.06)]">

    <h2 className="text-2xl font-semibold text-slate-900">
      Choose Template
    </h2>

    <p className="mt-2 text-sm leading-6 text-slate-500">
      Pick the presentation style that fits the role you are targeting, then export the tailored version as a PDF.
    </p>

    <div className="mt-6 space-y-3">

      {templates.map((item) => (
        <button
          key={item.id}
          onClick={() => setTemplate(item.id)}
          className={`w-full rounded-2xl border p-4 text-left transition ${
            template === item.id
              ? "border-teal-300 bg-teal-50 shadow-sm"
              : "border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50"
          }`}
        >
          <div className="flex items-center justify-between gap-3">
            <span className="text-base font-semibold text-slate-900">
              {item.name}
            </span>

            {template === item.id && (
              <span className="rounded-full bg-teal-600 px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] text-white">
                Active
              </span>
            )}
          </div>

          <p className="mt-2 text-sm leading-6 text-slate-500">
            {item.description}
          </p>
        </button>
      ))}

    </div>

    <button
      onClick={downloadPDF}
      className="mt-6 inline-flex w-full items-center justify-center rounded-2xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-teal-700"
    >
      Download PDF
    </button>

    <div className="mt-4 rounded-2xl bg-slate-50 p-4 text-sm leading-6 text-slate-600">
      Tip: choose the template that matches the company tone, then fine-tune the wording on the previous screen if needed.
    </div>

  </div>


  {/* RIGHT PANEL — RESUME PREVIEW */}

  <div className="rounded-[28px] border border-white/70 bg-[rgba(255,255,255,0.88)] p-6 shadow-[0_16px_44px_rgba(15,23,42,0.06)]">

    <div className="mb-5 flex flex-wrap items-center justify-between gap-4">
      <div>
        <h2 className="text-2xl font-semibold text-slate-900">
          Live Preview
        </h2>
        <p className="mt-1 text-sm leading-6 text-slate-500">
          Review the tailored resume before exporting it.
        </p>
      </div>

      <div className="rounded-full bg-slate-100 px-4 py-2 text-xs font-semibold uppercase tracking-[0.16em] text-slate-600">
        {templates.find((item) => item.id === template)?.name} template
      </div>
    </div>

    <div className="flex justify-center overflow-auto rounded-[24px] bg-slate-100/80 p-4 md:p-6">

      <div
        id="resume-preview"
        className="w-full max-w-[850px] min-h-[1000px] rounded-[12px] bg-white p-8 shadow-[0_20px_50px_rgba(15,23,42,0.12)] md:p-10"
      >

        {renderTemplate()}

      </div>
    </div>

  </div>

</div>


);
}

export default TemplateSelector;
