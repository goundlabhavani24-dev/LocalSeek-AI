# LocalSeek AI

## Offline AI-Powered Document Intelligence & Semantic Search

---

## Description

**LocalSeek AI** is an offline-first, CPU-optimized AI application that transforms unstructured local documents into structured, searchable knowledge. Instead of searching files only by filename, LocalSeek AI understands document content using local AI models and enables natural language search without requiring an internet connection.

The application processes PDF documents, images, and text files, extracts meaningful metadata, stores it in a local SQLite database, and allows users to quickly find documents based on their content.

This project is developed for the **CPU-First Hackathon**, demonstrating efficient AI inference that runs completely offline on CPU.

---

## Team Members

| Name               | Responsibility                                      |
| ------------------ | --------------------------------------------------- |
| **Dimple Kurella** | Frontend Development, AI Integration, Documentation |
| **Bhavani**        | Backend Development, Data Processing, Search Engine |

---

## Work Division

### 👩‍💻 Dimple Kurella

* Repository setup and project management
* README and project documentation
* Streamlit frontend
* File upload interface
* Search interface
* Dashboard
* Ollama (Llama 3.2) integration
* UI and backend integration
* Testing and presentation

### 👩‍💻 Bhavani

* PDF text extraction (PyMuPDF)
* OCR integration (Tesseract)
* Document classification
* Structured JSON generation
* SQLite database
* Search engine implementation
* JSON/CSV export
* Backend testing and optimization

---

## Features

* 📄 PDF document processing
* 🖼 OCR for scanned documents and images
* 🤖 Local AI inference using Llama 3.2
* 🔍 Natural language document search
* 🗄 SQLite local database
* 📤 Export structured data as JSON
* 🌐 Fully offline operation
* 💻 CPU-only inference

---

## Project Architecture

```text
User Folder
      │
      ▼
Document Discovery
      │
      ▼
Text Extraction
(PyMuPDF / OCR)
      │
      ▼
Document Classification
      │
      ▼
Local LLM (Llama 3.2)
      │
      ▼
Structured JSON
      │
      ▼
SQLite Database
      │
      ▼
Natural Language Search
```

---

## Technology Stack

| Component      | Technology         |
| -------------- | ------------------ |
| Frontend       | Streamlit          |
| Backend        | Python             |
| AI Model       | Ollama (Llama 3.2) |
| OCR            | Tesseract OCR      |
| PDF Processing | PyMuPDF            |
| Database       | SQLite             |

---

## Installation

### Prerequisites

* Python 3.11+
* Ollama
* Llama 3.2 Model
* Tesseract OCR

### Clone Repository

```bash
git clone https://code.swecha.org/dimplekurella/localseek-ai.git
cd localseek-ai
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Download Model

```bash
ollama pull llama3.2
```

### Run Application

```bash
streamlit run app.py
```

---

## Usage

1. Launch LocalSeek AI.
2. Upload documents or select a local folder.
3. The application extracts text using OCR or PDF parsing.
4. The local AI model classifies the document and generates structured metadata.
5. Metadata is stored in SQLite.
6. Search documents using natural language.
7. Export extracted data as JSON.

---

## Example Search Queries

* Find all invoices
* Show my medical reports
* Find certificates
* Search resumes with Python skills
* Show AI research papers

---

## Example Output

```json
{
  "document_type": "Invoice",
  "vendor": "ABC Store",
  "date": "2026-06-28",
  "total": 2450,
  "tags": [
    "invoice",
    "shopping"
  ]
}
```

---

## Project Structure

```text
LocalSeek-AI/

├── app.py
├── README.md
├── SPEC.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── requirements.txt
├── database/
├── models/
├── utils/
├── docs/
├── tests/
└── .gitlab-ci.yml
```

---

## Support

For questions, bug reports, or feature requests, please create an Issue in the GitLab repository.

---

## Roadmap

### Phase 1

* Repository setup
* Documentation
* Architecture design
* Project planning

### Phase 2

* PDF parsing
* OCR integration
* AI inference
* SQLite storage
* Search implementation

### Phase 3

* Dashboard
* JSON export
* Testing
* CI/CD
* Performance optimization

---

## Project Status

🚧 **Status:** Active Development

LocalSeek AI is currently under active development for the CPU-First Hackathon. Core features are being implemented, tested, and optimized for offline, CPU-only document intelligence and semantic search.

---

## Authors and Acknowledgment

**Authors**

* Dimple Kurella
* Bhavani

**Acknowledgment**

Thanks to the CPU-First Hackathon organizers and the open-source community for their support and tools.

---

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Run formatting and tests.
5. Submit a Merge Request.

---

## Development Commands

Run formatter

```bash
ruff format .
```

Run linter

```bash
ruff check .
```
License

This project is released under the GNU General Public License v3.0 (GPL-3.0) to comply with the hackathon requirement of using a strong copyleft Free and Open Source Software license.

## Authors and Acknowledgment

**Authors**

* Dimple Kurella
* Bhavani

**Acknowledgment**
Thanks to the CPU-First Hackathon organizers and the open-source community for their support and tools.

## Project Status

🚧 **Status:** Active Development

LocalSeek AI is currently under active development for the CPU-First Hackathon. Core features are being implemented, tested, and optimized for offline, CPU-only document intelligence and semantic search.

## Conclusion

LocalSeek AI demonstrates how AI can transform unstructured documents into structured, searchable knowledge using CPU-only, offline processing, providing a fast, private, and reliable document search experience.


Run type checking

```bash
mypy .
```

Run tests

```bash
pytest
```

