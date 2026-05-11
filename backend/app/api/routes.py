from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from app.services.resume_service import (
    generate_tailored_resume,
    generate_improved_resume_draft,
    generate_general_ats_review,
)
from app.services.text_extraction import (
    extract_text_from_docx,
    extract_text_from_pdf,
)

router = APIRouter()


class JobRequest(BaseModel):
    job_description: str
    resume_text: str | None = None


class ResumeReviewRequest(BaseModel):
    resume_text: str


@router.get("/health")
def health_check():
    return {"status": "API is working"}


@router.post("/generate-resume")
def generate_resume(request: JobRequest):

    if not request.resume_text or not request.resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Resume text is required for ATS analysis."
        )

    result = generate_tailored_resume(
        request.job_description,
        request.resume_text,
        include_improved_resume=False
    )

    return result


@router.post("/generate-improved-resume")
def generate_improved_resume(request: JobRequest):

    if not request.resume_text or not request.resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Resume text is required to build the improved resume."
        )

    improved_resume = generate_improved_resume_draft(
        request.job_description,
        request.resume_text
    )

    return {
        "improved_resume": improved_resume["text"],
        "improved_resume_data": improved_resume["structured"]
    }


@router.post("/general-ats-review")
def general_ats_review(request: ResumeReviewRequest):

    if not request.resume_text or not request.resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Resume text is required for a general ATS review."
        )

    return generate_general_ats_review(request.resume_text)


@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    filename = (file.filename or "").lower()

    if filename.endswith(".pdf"):
        text, extraction = extract_text_from_pdf(file.file)

    elif filename.endswith(".docx"):
        text, extraction = extract_text_from_docx(file.file)

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Please upload a PDF or DOCX file."
        )

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract readable text from the uploaded resume."
        )

    return {
        "resume_text": text,
        "extraction": extraction,
    }
