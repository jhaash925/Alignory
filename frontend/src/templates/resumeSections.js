const SECTION_PATTERN = /^(summary|skills|experience|projects|education)\s*:?\s*$/i;
const INLINE_SECTION_PATTERN = /(\*\*(summary|skills|experience|projects|education)\*\*|^(summary|skills|experience|projects|education)\s*:?\s*$)/gim;

function normalizeSectionTitle(line) {
  return line.trim().replace(/:$/, "").toUpperCase();
}

function isBulletLine(line) {
  return /^[-*•]/.test(line);
}

function cleanBullet(line) {
  return line.replace(/^[-*•]\s*/, "").trim();
}

function isContactLine(line) {
  return (
    /@/.test(line) ||
    /\b\d{10}\b/.test(line.replace(/\D/g, "")) ||
    /linkedin|github|portfolio|www\.|https?:\/\//i.test(line)
  );
}

function finalizeSection(section) {
  if (!section) return null;
  return { ...section, entries: section.entries.filter((e) => e.text) };
}

// ─── Structured-object path ──────────────────────────────────────────────────

function buildExperienceEntries(experience) {
  return (experience || []).flatMap((item) => {
    const bullets = (item.bullets || []).map((b) => ({ type: "bullet", text: b }));
    return [
      {
        type: "job",
        title: item.title || "",
        company: item.company || "",
        dates: item.dates || "",
        brief: item.brief || "",
        bullets,
      },
    ];
  });
}

function buildProjectEntries(projects) {
  return (projects || []).flatMap((item) => {
    const bullets = (item.bullets || []).map((b) => ({ type: "bullet", text: b }));
    return [
      {
        type: "project",
        name: item.name || "",
        subtitle: item.subtitle || "",
        brief: item.brief || "",
        bullets,
      },
    ];
  });
}

function buildSkillEntries(skills) {
  return (skills || []).map((group) => ({
    type: "skill_group",
    category: group.category || "Skills",
    items: group.items || [],
  }));
}

function buildEducationEntries(education) {
  return (education || []).map((item) => ({
    type: "education",
    text: item,
  }));
}

export function parseResumeDocument(resume) {
  // ── Structured object path ──
  if (resume && typeof resume === "object" && !Array.isArray(resume)) {
    const sections = [
      ...(resume.skills?.length
        ? [{ title: "SKILLS", entries: buildSkillEntries(resume.skills) }]
        : []),
      ...(resume.experience?.length
        ? [{ title: "EXPERIENCE", entries: buildExperienceEntries(resume.experience) }]
        : []),
      ...(resume.projects?.length
        ? [{ title: "PROJECTS", entries: buildProjectEntries(resume.projects) }]
        : []),
      ...(resume.education?.length
        ? [{ title: "EDUCATION", entries: buildEducationEntries(resume.education) }]
        : []),
    ];

    return {
      header: {
        name: resume.header?.name || "Candidate Name",
        contact: resume.header?.contact || [],
        headline: resume.summary || resume.header?.headline || "",
      },
      sections,
    };
  }

  // ── Plain-text fallback path ──
  const normalizedResume = (resume || "")
    .replace(/\r/g, "\n")
    .replace(
      INLINE_SECTION_PATTERN,
      (match) =>
        `\n${match.replace(/\*\*/g, "").replace(/:$/, "").toUpperCase()}\n`
    );

  const lines = normalizedResume
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);

  const headerLines = [];
  const sections = [];
  let currentSection = null;

  for (const line of lines) {
    if (SECTION_PATTERN.test(line)) {
      const finalized = finalizeSection(currentSection);
      if (finalized) sections.push(finalized);
      currentSection = { title: normalizeSectionTitle(line), entries: [] };
      continue;
    }

    if (!currentSection) {
      headerLines.push(line);
      continue;
    }

    currentSection.entries.push({
      text: isBulletLine(line) ? cleanBullet(line) : line,
      type: isBulletLine(line) ? "bullet" : "paragraph",
    });
  }

  const finalized = finalizeSection(currentSection);
  if (finalized) sections.push(finalized);

  const name = headerLines[0] || "Candidate Name";
  const contactLines = headerLines.slice(1).filter(isContactLine);
  const introLines = headerLines.slice(1).filter((l) => !isContactLine(l));

  return {
    header: {
      name,
      contact: contactLines,
      headline: introLines.join(" "),
    },
    sections,
  };
}

export function parseResumeSections(resume) {
  return parseResumeDocument(resume).sections;
}
