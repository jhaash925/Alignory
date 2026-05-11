// ─── Contact Row ─────────────────────────────────────────────────────────────

export function ContactRow({ contact, tone = "slate" }) {
  if (!contact || contact.length === 0) return null;
  const colorMap = {
    slate: "text-slate-500",
    teal: "text-teal-700",
    white: "text-slate-200",
  };
  return (
    <div className={`flex flex-wrap items-center gap-x-4 gap-y-1 text-[11px] font-medium ${colorMap[tone] || colorMap.slate}`}>
      {contact.map((item, i) => (
        <span key={i} className="flex items-center gap-1.5">
          {i > 0 && <span className="opacity-40">·</span>}
          {item}
        </span>
      ))}
    </div>
  );
}

// ─── Job Entry ────────────────────────────────────────────────────────────────

export function JobEntry({ entry, accentColor = "text-slate-900", dateColor = "text-slate-500", bulletDot = "bg-teal-600" }) {
  return (
    <div className="mb-4 last:mb-0">
      <div className="flex items-baseline justify-between gap-4">
        <div className={`text-[13px] font-bold leading-tight ${accentColor}`}>
          {entry.title}
        </div>
        {entry.dates && (
          <div className={`shrink-0 text-[11px] font-medium ${dateColor}`}>
            {entry.dates}
          </div>
        )}
      </div>
      {entry.company && (
        <div className="mt-0.5 text-[12px] font-medium text-slate-500 italic">
          {entry.company}
        </div>
      )}
      {entry.brief && (
        <p className="mt-1.5 text-[12px] leading-[1.55] text-slate-600">
          {entry.brief}
        </p>
      )}
      {entry.bullets?.length > 0 && (
        <ul className="mt-2 space-y-1">
          {entry.bullets.map((b, i) => (
            <li key={i} className="flex gap-2.5 text-[12px] leading-[1.55] text-slate-700">
              <span className={`mt-[7px] h-1.5 w-1.5 shrink-0 rounded-full ${bulletDot}`} />
              <span>{b.text ?? b}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

// ─── Project Entry ────────────────────────────────────────────────────────────

export function ProjectEntry({ entry, accentColor = "text-slate-900", bulletDot = "bg-teal-600" }) {
  return (
    <div className="mb-4 last:mb-0">
      <div className="flex items-baseline gap-2">
        <div className={`text-[13px] font-bold leading-tight ${accentColor}`}>
          {entry.name}
        </div>
        {entry.subtitle && (
          <div className="text-[11.5px] font-medium text-slate-500">
            — {entry.subtitle}
          </div>
        )}
      </div>
      {entry.brief && (
        <p className="mt-1.5 text-[12px] leading-[1.55] text-slate-600">
          {entry.brief}
        </p>
      )}
      {entry.bullets?.length > 0 && (
        <ul className="mt-2 space-y-1">
          {entry.bullets.map((b, i) => (
            <li key={i} className="flex gap-2.5 text-[12px] leading-[1.55] text-slate-700">
              <span className={`mt-[7px] h-1.5 w-1.5 shrink-0 rounded-full ${bulletDot}`} />
              <span>{b.text ?? b}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

// ─── Skills Grid (pill style) ─────────────────────────────────────────────────

export function SkillsGrid({
  entries,
  pillBg = "bg-slate-100",
  pillText = "text-slate-700",
  labelColor = "text-teal-700",
  variant = "rows",
}) {
  // Support both "entries" array (from resumeSections typed output)
  // and legacy "groups" prop for backwards compat
  const groups = entries || [];
  if (groups.length === 0) return null;

  if (variant === "rows") {
    return (
      <div className="space-y-1.5">
        {groups.map((group, i) => {
          const itemsText = (group.items || []).join(" • ");

          return (
            <div key={i} className="grid gap-x-3 gap-y-0.5 sm:grid-cols-[190px_1fr]">
              <div className={`text-[10.5px] font-bold uppercase tracking-[0.16em] ${labelColor}`}>
                {group.category}
              </div>

              <div className="text-[12px] leading-[1.45] text-slate-700">
                {itemsText}
              </div>
            </div>
          );
        })}
      </div>
    );
  }

  return (
    <div className="space-y-2.5">
      {groups.map((group, i) => (
        <div key={i} className="flex flex-wrap items-start gap-x-3 gap-y-1.5">
          <div className={`mt-0.5 w-[130px] shrink-0 text-[10px] font-bold uppercase tracking-[0.22em] ${labelColor}`}>
            {group.category}
          </div>
          <div className="flex flex-1 flex-wrap gap-1.5">
            {(group.items || []).map((skill, j) => (
              <span
                key={j}
                className={`rounded-md px-2 py-0.5 text-[11px] font-medium ${pillBg} ${pillText}`}
              >
                {skill}
              </span>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

// ─── Education Entry ──────────────────────────────────────────────────────────

export function EducationEntry({ entry }) {
  const text = String(entry.text || "").trim();
  const match = text.match(/^(.*?)(\b(?:19|20)\d{2}\s*[–-]\s*\d{2,4})$/);

  if (match) {
    const [, label, dates] = match;
    return (
      <div className="flex items-baseline justify-between gap-4 text-[12px] leading-[1.55] text-slate-700">
        <span>{label.trim()}</span>
        <span className="shrink-0 font-semibold text-slate-800">{dates.trim()}</span>
      </div>
    );
  }

  return (
    <p className="text-[12px] leading-[1.55] text-slate-700">
      {text}
    </p>
  );
}

// ─── Plain-text fallback paragraph / bullet ───────────────────────────────────

export function ParagraphEntry({ entry, bulletDot = "bg-teal-600" }) {
  if (entry.type === "bullet") {
    return (
      <div className="flex gap-2.5 text-[12px] leading-[1.55] text-slate-700">
        <span className={`mt-[7px] h-1.5 w-1.5 shrink-0 rounded-full ${bulletDot}`} />
        <span>{entry.text}</span>
      </div>
    );
  }
  return (
    <p className="text-[13px] font-semibold leading-tight text-slate-800">
      {entry.text}
    </p>
  );
}

// ─── Universal Section Renderer ───────────────────────────────────────────────

export function SectionEntries({
  entries = [],
  bulletDot = "bg-teal-600",
  accentColor = "text-slate-900",
  dateColor = "text-slate-500",
  pillBg = "bg-slate-100",
  pillText = "text-slate-700",
  labelColor = "text-teal-700",
  skillsVariant = "rows",
}) {
  // Group consecutive bullets under their job/project parent naturally —
  // they are already embedded inside job/project entries in the new data model.
  return (
    <div className="space-y-0.5">
      {entries.map((entry, i) => {
        switch (entry.type) {
          case "job":
            return (
              <JobEntry
                key={i}
                entry={entry}
                accentColor={accentColor}
                dateColor={dateColor}
                bulletDot={bulletDot}
              />
            );
          case "project":
            return (
              <ProjectEntry
                key={i}
                entry={entry}
                accentColor={accentColor}
                bulletDot={bulletDot}
              />
            );
          case "skill_group":
            return (
              <SkillsGrid
                key={i}
                entries={[entry]}
                pillBg={pillBg}
                pillText={pillText}
                labelColor={labelColor}
                variant={skillsVariant}
              />
            );
          case "education":
            return <EducationEntry key={i} entry={entry} />;
          default:
            return (
              <ParagraphEntry key={i} entry={entry} bulletDot={bulletDot} />
            );
        }
      })}
    </div>
  );
}
