import os
import requests

# GitLab API configuration
GITLAB_URL = "https://code.swecha.org/api/v4"
PROJECT_ID = 70591

# Prompt for Personal Access Token securely
GITLAB_TOKEN = os.environ.get("GITLAB_TOKEN")
if not GITLAB_TOKEN:
    print("----------------------------------------------------------------------")
    print("Swecha GitLab requires a Personal Access Token (PAT) for API writes.")
    print(
        "You can generate one under: User Settings -> Access Tokens (with 'api' scope)."
    )
    print("----------------------------------------------------------------------")
    try:
        GITLAB_TOKEN = input("Please paste your Swecha GitLab PAT: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting script.")
        exit(1)

if not GITLAB_TOKEN:
    print("No token provided. Exiting.")
    exit(1)

HEADERS = {"PRIVATE-TOKEN": GITLAB_TOKEN}

# Detailed hackathon issues
issues_data = [
    {
        "title": "Backend PDF Text Extraction Engine (PyMuPDF)",
        "description": "Develop a backend module to extract text content page-by-page from local PDFs.\n\nTasks:\n- Implement app/pdf_parser.py\n- Use PyMuPDF library\n- Include unit tests",
        "assignee_ids": [103433],  # Bhavani
        "due_date": "2026-06-28",
        "estimate": "2h",
    },
    {
        "title": "OCR Image Parsing Engine (Tesseract)",
        "description": "Implement OCR text extraction for local PNG/JPG files using Tesseract OCR.\n\nTasks:\n- Implement app/ocr_engine.py\n- Convert images to grayscale for CPU accuracy\n- Handle missing Tesseract gracefully\n- Add unit tests",
        "assignee_ids": [103433],  # Bhavani
        "due_date": "2026-06-28",
        "estimate": "3h",
    },
    {
        "title": "SQLite Database Design & Storage helper",
        "description": "Design schema for local structured metadata and implement DBManager.\n\nTasks:\n- Implement database/db_manager.py\n- SQLite tables: documents, document_tags\n- Content hash-based document IDs\n- Implement full-text-search retrieval",
        "assignee_ids": [103433],  # Bhavani
        "due_date": "2026-06-28",
        "estimate": "4h",
    },
    {
        "title": "Document Classification & Metadata Extractor Fallback",
        "description": "Integrate local Ollama Llama 3.2 and implement a local rule-based heuristic fallback.\n\nTasks:\n- Implement app/llm_client.py\n- Standard prompt template for structured JSON\n- Rule-based parser for offline fallback without Ollama\n- Unit tests for both paths",
        "assignee_ids": [103433],  # Bhavani
        "due_date": "2026-06-28",
        "estimate": "4h",
    },
    {
        "title": "Integration Pipeline & Keyword Search Logic",
        "description": "Bind extraction engines, database storage, and classification under a single pipeline.\n\nTasks:\n- Implement app/pipeline.py\n- Cache check via file hash\n- Directory scanning support\n- Connect search queries to backend",
        "assignee_ids": [103433],  # Bhavani
        "due_date": "2026-06-28",
        "estimate": "3h",
    },
    {
        "title": "Streamlit UI Base & Multi-page Navigation",
        "description": "Develop Streamlit multi-page container and clean dark-mode navigation sidebar.\n\nTasks:\n- Implement frontend/main.py\n- Navigation between Home, Upload, Search, and Dashboard views",
        "assignee_ids": [103255],  # Dimple
        "due_date": "2026-06-28",
        "estimate": "3h",
    },
    {
        "title": "Document Ingestion & Upload Interface",
        "description": "Create document uploader view with real-time feedback and processing spinners.\n\nTasks:\n- Implement frontend/views/upload.py\n- Integration with DocumentPipeline\n- Cache warning display\n- Metadata JSON presentation",
        "assignee_ids": [103255],  # Dimple
        "due_date": "2026-06-28",
        "estimate": "4h",
    },
    {
        "title": "Search & CSV/JSON Export View",
        "description": "Implement keyword and tag search query interface with export triggers.\n\nTasks:\n- Implement frontend/views/search.py\n- Results cards formatting\n- Export to JSON and CSV formats",
        "assignee_ids": [103255],  # Dimple
        "due_date": "2026-06-28",
        "estimate": "3h",
    },
    {
        "title": "CI/CD Pipeline Setup & Repo Quality Checks",
        "description": "Set up GitLab CI workflow and pre-commit automation with 10+ distinct checks.\n\nTasks:\n- Configure .pre-commit-config.yaml\n- Configure .gitlab-ci.yml stages\n- Run formatting, lint, typecheck, security scans",
        "assignee_ids": [103255],  # Dimple
        "due_date": "2026-06-28",
        "estimate": "4h",
    },
    {
        "title": "Final Documentation & Walkthrough Guide",
        "description": "Prepare repo documentation and walkthrough guide showing test runs.\n\nTasks:\n- Write README.md, SPEC.md, WORK_DIVISION.md\n- Write CONTRIBUTING.md, CHANGELOG.md\n- Create walkthrough.md with validation outputs",
        "assignee_ids": [103433],  # Bhavani
        "due_date": "2026-06-28",
        "estimate": "2h",
    },
]


def get_existing_issues():
    url = f"{GITLAB_URL}/projects/{PROJECT_ID}/issues"
    response = requests.get(url, headers=HEADERS, timeout=10)
    if response.status_code == 200:
        return [issue["title"] for issue in response.json()]
    else:
        print(
            f"Failed to fetch existing issues: {response.status_code} {response.text}"
        )
        return []


def create_issue(issue_info):
    url = f"{GITLAB_URL}/projects/{PROJECT_ID}/issues"
    payload = {
        "title": issue_info["title"],
        "description": issue_info["description"],
        "assignee_ids": issue_info["assignee_ids"],
        "due_date": issue_info["due_date"],
    }
    response = requests.post(url, json=payload, headers=HEADERS, timeout=10)
    if response.status_code in (200, 201):
        created_issue = response.json()
        print(
            f"Successfully created issue: '{issue_info['title']}' (IID: {created_issue['iid']})"
        )
        return created_issue["iid"]
    else:
        print(
            f"Failed to create issue '{issue_info['title']}': {response.status_code} {response.text}"
        )
        return None


def set_estimate(issue_iid, duration):
    url = f"{GITLAB_URL}/projects/{PROJECT_ID}/issues/{issue_iid}/time_estimate"
    payload = {"duration": duration}
    response = requests.post(url, json=payload, headers=HEADERS, timeout=10)
    if response.status_code == 200:
        print(f"  Successfully set time estimate to {duration} for issue #{issue_iid}")
    else:
        print(
            f"  Failed to set estimate for issue #{issue_iid}: {response.status_code} {response.text}"
        )


def main():
    print("Fetching existing issues to prevent duplicates...")
    existing = get_existing_issues()
    if not existing and len(HEADERS["PRIVATE-TOKEN"]) > 0:
        # Check if auth failed
        pass

    for issue in issues_data:
        if issue["title"] in existing:
            print(f"Skipping issue: '{issue['title']}' (already exists)")
            continue

        iid = create_issue(issue)
        if iid:
            set_estimate(iid, issue["estimate"])

    print("Done processing hackathon issues!")


if __name__ == "__main__":
    main()
