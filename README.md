# Alignory

Alignory is an AI resume tailoring app that reviews a resume against a job description, scores ATS alignment, highlights matched and missing skills, and generates a stronger resume draft.

The project is split into a FastAPI backend and a React/Vite frontend.

## Features

- Upload PDF or DOCX resumes and extract resume text.
- Run job-specific ATS analysis with matched skills, missing skills, and scoring.
- Generate an improved resume draft for a target job description.
- Run a general ATS review without a job description.
- Preview resume content in multiple templates.
- Export resume output from the frontend.

## Tech Stack

- Backend: FastAPI, Python, pdfplumber, python-docx, scikit-learn, LangChain, ChromaDB, Ollama
- Frontend: React, Vite, Tailwind CSS, React Router
- Local AI: Ollama with the `llama3` model

## Project Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── rag/
│   │   ├── services/
│   │   └── utils/
│   ├── benchmarks/
│   ├── data/
│   ├── requirements.txt
│   └── scripts/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── templates/
│   └── package.json
├── package.json
└── README.md
```

## Prerequisites

- Python 3.11+
- Node.js 20+
- npm
- Ollama installed and running locally

Pull the local model used by the backend:

```bash
ollama pull llama3
```

## Backend Setup

From the repository root:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at:

```text
http://127.0.0.1:8000
```

Useful endpoints:

- `GET /health`
- `POST /upload-resume`
- `POST /generate-resume`
- `POST /generate-improved-resume`
- `POST /general-ats-review`

## Frontend Setup

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend usually runs at:

```text
http://127.0.0.1:5173
```

The frontend currently calls the backend at `http://127.0.0.1:8000`.

## Development

Run the frontend linter:

```bash
cd frontend
npm run lint
```

Run the ATS benchmark script:

```bash
cd backend
python scripts/run_ats_benchmarks.py
```

## Notes

- Keep local secrets in `.env` files. They are ignored by Git.
- `node_modules`, Python bytecode, and OS metadata files are ignored.
- The backend CORS policy is open for local development and should be restricted before production deployment.
