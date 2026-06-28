# LocalSeek AI - Project Issues (GitLab Issues)

This document lists the 10 project issues created in GitLab to track progress during the CPU-First Hackathon, complete with assignees, time estimates, and due dates.

---

## Issues Summary Table

| # | Issue Title | Assignee | Estimate | Due Date | Status |
| :--- | :--- | :--- | :---: | :---: | :---: |
| 1 | **Initialize repository & project structure** | Dimple Kurella (`@dimplekurella`) | 30 min | 2026-06-28 | Pending |
| 2 | **Write README and SPEC** | Dimple Kurella (`@dimplekurella`) | 45 min | 2026-06-28 | Pending |
| 3 | **Build Streamlit UI** | Dimple Kurella (`@dimplekurella`) | 2 hours | 2026-06-28 | Pending |
| 4 | **Integrate Ollama (Llama 3.2)** | Dimple Kurella (`@dimplekurella`) | 1.5 hours | 2026-06-28 | Pending |
| 5 | **Implement PDF text extraction** | Bhavani (`@Bhavani25`) | 1 hour | 2026-06-28 | Pending |
| 6 | **Implement OCR for images** | Bhavani (`@Bhavani25`) | 1 hour | 2026-06-28 | Pending |
| 7 | **Create document classification & JSON extraction** | Bhavani (`@Bhavani25`) | 2 hours | 2026-06-28 | Pending |
| 8 | **Design SQLite database & search** | Bhavani (`@Bhavani25`) | 1.5 hours | 2026-06-28 | Pending |
| 9 | **Integration, testing & bug fixes** | Both (`@dimplekurella`, `@Bhavani25`) | 1 hour | 2026-06-28 | Pending |
| 10 | **Documentation, CI checks & final demo** | Both (`@dimplekurella`, `@Bhavani25`) | 1 hour | 2026-06-28 | Pending |

---

## Detailed Issue Descriptions

### 1. Initialize repository & project structure
* **Assignee:** Dimple Kurella (`@dimplekurella`)
* **Estimate:** 30 minutes (`/estimate 30m`)
* **Due Date:** 2026-06-28 (`/due 2026-06-28`)
* **Description:** Initialize the project folders and create baseline files:
  * Directories: `app/`, `database/`, `models/`, `docs/`, `tests/`
  * Files: `LICENSE`, `CONTRIBUTING.md`, `CHANGELOG.md`, `.gitignore`, `.gitlab-ci.yml`

### 2. Write README and SPEC
* **Assignee:** Dimple Kurella (`@dimplekurella`)
* **Estimate:** 45 minutes (`/estimate 45m`)
* **Due Date:** 2026-06-28 (`/due 2026-06-28`)
* **Description:** Create documentation for Phase 1 detailing specifications, objectives, architecture flow, and usage guides in `README.md` and `SPEC.md`.

### 3. Build Streamlit UI
* **Assignee:** Dimple Kurella (`@dimplekurella`)
* **Estimate:** 2 hours (`/estimate 2h`)
* **Due Date:** 2026-06-28 (`/due 2026-06-28`)
* **Description:** Develop the frontend client in Streamlit:
  * Folder selector and file upload widget.
  * Status and progress tracker during document parsing.
  * Search input bar with filters.
  * Extracted metadata display (card-based view) and file link download.

### 4. Integrate Ollama (Llama 3.2)
* **Assignee:** Dimple Kurella (`@dimplekurella`)
* **Estimate:** 1.5 hours (`/estimate 1h 30m`)
* **Due Date:** 2026-06-28 (`/due 2026-06-28`)
* **Description:** Configure connection to local Ollama service:
  * Pull Llama 3.2 model locally.
  * Create prompt templates for document analysis and information extraction.
  * Set up structured text outputs matching our JSON metadata schema.

### 5. Implement PDF text extraction
* **Assignee:** Bhavani (`@Bhavani25`)
* **Estimate:** 1 hour (`/estimate 1h`)
* **Due Date:** 2026-06-28 (`/due 2026-06-28`)
* **Description:** Write python parsing logic using `PyMuPDF` to read local PDF files and extract raw text for LLM ingestion. Handle multi-page documents and exceptions.

### 6. Implement OCR for images
* **Assignee:** Bhavani (`@Bhavani25`)
* **Estimate:** 1 hour (`/estimate 1h`)
* **Due Date:** 2026-06-28 (`/due 2026-06-28`)
* **Description:** Integrate `Tesseract OCR` to extract text from images (PNG, JPG, scanned PDFs). Setup pre-processing steps (grayscale, binarization) to optimize accuracy on CPU.

### 7. Create document classification & JSON extraction
* **Assignee:** Bhavani (`@Bhavani25`)
* **Estimate:** 2 hours (`/estimate 2h`)
* **Due Date:** 2026-06-28 (`/due 2026-06-28`)
* **Description:** Build extraction pipeline:
  * Format extracted text to feed to Llama 3.2.
  * Enforce strict JSON output parsing (document type, title, tags, summary, etc.).
  * Validate JSON output against standard schema.

### 8. Design SQLite database & search
* **Assignee:** Bhavani (`@Bhavani25`)
* **Estimate:** 1.5 hours (`/estimate 1h 30m`)
* **Due Date:** 2026-06-28 (`/due 2026-06-28`)
* **Description:** Design database and query engine:
  * Define table schema for processed documents and metadata.
  * Write SQLite helper functions for insertion and retrieval.
  * Implement query parsing and match scoring for natural language search.

### 9. Integration, testing & bug fixes
* **Assignee:** Both (`@dimplekurella`, `@Bhavani25`)
* **Estimate:** 1 hour (`/estimate 1h`)
* **Due Date:** 2026-06-28 (`/due 2026-06-28`)
* **Description:** Connect the UI and backend:
  * Integrate backend processing scripts into Streamlit.
  * Debug and resolve data flow and interface issues.
  * Verify that indexing and search work entirely offline with Wi-Fi disabled.

### 10. Documentation, CI checks & final demo
* **Assignee:** Both (`@dimplekurella`, `@Bhavani25`)
* **Estimate:** 1 hour (`/estimate 1h`)
* **Due Date:** 2026-06-28 (`/due 2026-06-28`)
* **Description:** Complete project wrap-up:
  * Write `walkthrough.md` with screenshots/logs.
  * Set up GitLab CI `.gitlab-ci.yml` linting checks.
  * Run and polish final demonstration scripts.
