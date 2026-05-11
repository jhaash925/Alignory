export async function generateResume(jobDescription, resumeText) {

  const response = await fetch("http://127.0.0.1:8000/generate-resume", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      job_description: jobDescription,
      resume_text: resumeText
    })
  });

  if (!response.ok) {
    const errorPayload = await response.json().catch(() => ({}));
    throw new Error(errorPayload.detail || "ATS analysis failed");
  }

  const data = await response.json();

  return data;
}
