# LocalSeek AI - Project Issues (GitLab Issues)

This document lists the 10 project issues created in GitLab to track progress during the CPU-First Hackathon, complete with assignees, time estimates, and due dates.

---

## Issues Summary Table

| # | Issue Title | Assignee | Estimate | Due Date | Status |
| :--- | :--- | :--- | :---: | :---: | :---: |
| 1 | **Repository Setup** | Dimple Kurella (`@dimplekurella`) | 30 min | 2026-06-28 | Pending |
| 2 | **Create Streamlit UI** | Dimple Kurella (`@dimplekurella`) | 2 hours | 2026-06-28 | Pending |
| 3 | **Implement PDF Text Extraction** | Bhavani (`@Bhavani25`) | 1 hour | 2026-06-28 | Pending |
| 4 | **Implement OCR for Images** | Bhavani (`@Bhavani25`) | 1 hour | 2026-06-28 | Pending |
| 5 | **Integrate Ollama (Llama 3.2)** | Dimple Kurella (`@dimplekurella`) | 1.5 hours | 2026-06-28 | Pending |
| 6 | **Design SQLite Database** | Bhavani (`@Bhavani25`) | 1 hour | 2026-06-28 | Pending |
| 7 | **Generate Structured JSON** | Bhavani (`@Bhavani25`) | 1.5 hours | 2026-06-28 | Pending |
| 8 | **Implement Search Functionality** | Dimple Kurella (`@dimplekurella`) | 1 hour | 2026-06-28 | Pending |
| 9 | **Testing & Bug Fixes** | Both (`@dimplekurella`, `@Bhavani25`) | 1 hour | 2026-06-28 | Pending |
| 10 | **Final Integration & Documentation** | Both (`@dimplekurella`, `@Bhavani25`) | 1 hour | 2026-06-28 | Pending |

---

## Detailed Issue Descriptions

### 1. Repository Setup
* **Assignee:** Dimple Kurella (`@dimplekurella`)
* **Estimate:** 30 minutes (`/estimate 30m`)
* **Due Date:** 2026-06-28 (`/due 2026-06-28`)
* **Description:** Initialize the project folders and create baseline files:
  * Directories: `app/`, `database/`, `models/`, `docs/`, `tests/`
  * Files: `LICENSE`, `CONTRIBUTING.md`, `CHANGELOG.md`, `.gitignore`, `.gitlab-ci.yml`

### 2. Create Streamlit UI
* **Assignee:** Dimple Kurella (`@dimplekurella`)
* **Estimate:** 2 hours (`/estimate 2h`)
* **Due Date:** 2026-06-28 (`/due 2026-06-28`)
* **Description:** Develop the frontend client in Streamlit:
  * Folder selector and file upload widget.
  * Status and progress tracker during document parsing.
  * Search input bar with filters.
  * Extracted metadata display (card-based view) and file link download.

### 3. Implement PDF Text Extraction
* **Assignee:** Bhavani (`@Bhavani25`)
* **Estimate:** 1 hour (`/estimate 1h`)
* **Due Date:** 2026-06-28 (`/due 2026-06-28`)
* **Description:** Write python parsing logic using `PyMuPDF` to read local PDF files and extract raw text for LLM ingestion. Handle multi-page documents and exceptions.

### 4. Implement OCR for Images
* **Assignee:** Bhavani (`@Bhavani25`)
* **Estimate:** 1 hour (`/estimate 1h`)
* **Due Date:** 2026-06-28 (`/due 2026-06-28`)
* **Description:** Integrate `Tesseract OCR` to extract text from images (PNG, JPG, scanned PDFs). Setup pre-processing steps (grayscale, binarization) to optimize accuracy on CPU.

### 5. Integrate Ollama (Llama 3.2)
* **Assignee:** Dimple Kurella (`@dimplekurella`)
* **Estimate:** 1.5 hours (`/estimate 1h 30m`)
* **Due Date:** 2026-06-28 (`/due 2026-06-28`)
* **Description:** Configure connection to local Ollama service:
  * Pull Llama 3.2 model locally.
  * Create prompt templates for document analysis and information extraction.
  * Set up structured text outputs matching our JSON metadata schema.

### 6. Design SQLite Database
* **Assignee:** Bhavani (`@Bhavani25`)
* **Estimate:** 1 hour (`/estimate 1h`)
* **Due Date:** 2026-06-28 (`/due 2026-06-28`)
* **Description:** Design database:
  * Define table schema for processed documents and metadata.
  * Write SQLite helper functions for insertion and retrieval.

### 7. Generate Structured JSON
* **Assignee:** Bhavani (`@Bhavani25`)
* **Estimate:** 1.5 hours (`/estimate 1h 30m`)
* **Due Date:** 2026-06-28 (`/due 2026-06-28`)
* **Description:** Build extraction pipeline:
  * Format extracted text to feed to Llama 3.2.
  * Enforce strict JSON output parsing (document type, title, tags, summary, etc.).
  * Validate JSON output against standard schema.

### 8. Implement Search Functionality
* **Assignee:** Dimple Kurella (`@dimplekurella`)
* **Estimate:** 1 hour (`/estimate 1h`)
* **Due Date:** 2026-06-28 (`/due 2026-06-28`)
* **Description:** Implement the search engine logic including keyword and natural language queries to retrieve documents and metadata, and hook it up to the frontend UI.

### 9. Testing & Bug Fixes
* **Assignee:** Both (`@dimplekurella`, `@Bhavani25`)
* **Estimate:** 1 hour (`/estimate 1h`)
* **Due Date:** 2026-06-28 (`/due 2026-06-28`)
* **Description:** Connect the UI and backend:
  * Integrate backend processing scripts into Streamlit.
  * Debug and resolve data flow and interface issues.
  * Verify that indexing and search work entirely offline with Wi-Fi disabled.

### 10. Final Integration & Documentation
* **Assignee:** Both (`@dimplekurella`, `@Bhavani25`)
* **Estimate:** 1 hour (`/estimate 1h`)
* **Due Date:** 2026-06-28 (`/due 2026-06-28`)
* **Description:** Complete project wrap-up:
  * Write `walkthrough.md` with screenshots/logs.
  * Set up GitLab CI `.gitlab-ci.yml` linting checks.
  * Run and polish final demonstration scripts.
