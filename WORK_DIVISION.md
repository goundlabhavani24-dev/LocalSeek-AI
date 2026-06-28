# LocalSeek AI - Work Division Plan

This document outlines the division of work between the team members for the development of **LocalSeek AI** during the CPU-First Hackathon.

## Team Members

* **Dimple Kurella (Member 1)** - AI Integration, Frontend Development, Documentation
* **Bhavani (Member 2)** - Backend Development, Data Processing, Search Engine

---

## Task Assignment Matrix

| Task | Member 1 (Dimple) | Member 2 (Bhavani) | Status |
| :--- | :---: | :---: | :---: |
| **Project Setup & Git Repository Initialization** | ✅ | | Completed |
| **README, LICENSE & Initial Documentation** | ✅ | | Completed |
| **Streamlit UI Design & Implementation** | ✅ | | Pending |
| **Upload Documents / Folder Selection Interface** | ✅ | | Pending |
| **Search & Results Interface** | ✅ | | Pending |
| **Dashboard & Analytics View** | ✅ | | Pending |
| **Integrate Backend with Streamlit UI** | ✅ | | Pending |
| **Ollama / Llama 3.2 Integration & Inference** | ✅ | | Pending |
| **PDF Text Extraction Backend (PyMuPDF)** | | ✅ | Pending |
| **OCR Backend for Images (Tesseract)** | | ✅ | Pending |
| **Document Classification Logic** | | ✅ | Pending |
| **Structured JSON Metadata Generation** | | ✅ | Pending |
| **SQLite Database Design & Integration** | | ✅ | Pending |
| **Search Engine & Retrieval Logic** | | ✅ | Pending |
| **JSON/CSV Export Feature** | | ✅ | Pending |
| **Integration & Unit Testing** | ✅ | ✅ | Pending |
| **CI/CD Pipeline Setup (.gitlab-ci.yml)** | ✅ | ✅ | Pending |
| **Final Documentation & Walkthrough** | ✅ | ✅ | Pending |
| **Demo Script & Presentation Prep** | ✅ | ✅ | Pending |

---

## Detailed Member Responsibilities

### 🧑‍💻 Member 1 – Dimple Kurella (AI Integration & Frontend)

#### Phase 1: Repository & Setup
* Initialize GitLab repository and project structure.
* Write initial documentation (`README.md`, `SPEC.md`).
* Define and structure user flow.

#### Phase 2: UI & AI Integration
* Create the Streamlit application base.
* Implement file upload and folder selection screens.
* Design the search dashboard and results view.
* Connect local Ollama (Llama 3.2) inference.
* Interface frontend views with the data processing backend.

#### Phase 3: Verification & Delivery
* Conduct integration testing.
* Set up GitLab CI/CD workflow pipeline.
* Finalize demonstration plan and presentation slides.

---

### 👩‍💻 Member 2 – Bhavani (Backend & Data Processing)

#### Phase 1: Architecture & DB Design
* Define structured JSON metadata schemas.
* Design SQLite database tables and indexes.
* Plan the text extraction and OCR pipeline.

#### Phase 2: Backend Development
* Implement PDF parser using PyMuPDF.
* Integrate Tesseract OCR for document image parsing.
* Implement document classification (Invoice, Resume, Medical, Certificate, Notes, etc.).
* Develop metadata extraction logic (structured JSON generator).
* Implement SQLite database storage, queries, and search logic.
* Implement JSON/CSV export functionality.

#### Phase 3: Verification & Delivery
* Write unit and performance tests.
* Optimize indexing performance for CPU-first execution.
* Support front-end integration and bug fixing.

---

## Suggested Hackathon Timeline

| Time Slot | Member 1 (Dimple) | Member 2 (Bhavani) |
| :--- | :--- | :--- |
| **08:00 – 10:00** | Repo initialization, README, SPEC, UI wireframing | Database design, JSON schemas, processing flow |
| **10:00 – 12:30** | Build Streamlit UI components, Ollama basic setup | PDF parsing engine, OCR setup, SQLite helper class |
| **12:30 – 14:00** | Create Search views, build analytics dashboard | Classification, Metadata generation, JSON builder |
| **14:00 – 15:00** | Integration of UI and Backend modules | Integration support, database queries integration |
| **15:00 – 16:00** | Testing, resolving interface bugs | Testing, fixing backend issues, optimizing |
| **16:00 – 17:00** | Finalize GitLab CI, write user documentation | Code cleanup, format checking, project documentation |
| **17:00 – End** | Demo video recording, presentation preparation | Demo run support, final verification |
