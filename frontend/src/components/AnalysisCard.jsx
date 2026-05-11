import ReactMarkdown from "react-markdown";

function AnalysisCard({ analysis }) {

  return (

    <div className="overflow-hidden rounded-[28px] border border-white/70 bg-[rgba(255,255,255,0.9)] p-6 shadow-[0_18px_48px_rgba(15,23,42,0.08)]">

      <div className="mb-4">
        <h2 className="text-2xl font-semibold text-slate-900">
          Resume Analysis
        </h2>
        <p className="mt-1 text-sm text-slate-500">
          Plain-language guidance generated from your ATS match results.
        </p>
      </div>

      <div className="prose max-w-none prose-headings:text-slate-900 prose-p:text-slate-700 prose-strong:text-slate-900">

        <ReactMarkdown>
          {analysis}
        </ReactMarkdown>

      </div>

    </div>

  );
}

export default AnalysisCard;
