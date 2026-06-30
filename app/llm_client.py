import json
import requests
from typing import Any


class OllamaClient:
    """
    Client wrapper for local Ollama (Llama 3.2) inference on CPU.
    """

    def __init__(self, host: str = "http://localhost:11434", model: str = "llama3.2"):
        self.host = host.rstrip("/")
        self.model = model

    def check_connection(self) -> bool:
        """
        Check if the local Ollama service is running and accessible.
        """
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=3)
            return response.status_code == 200
        except Exception:
            return False

    def pull_model_if_missing(self) -> bool:
        """
        Check if the configured model is installed, and trigger a pull if not.
        """
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            if response.status_code == 200:
                tags = response.json().get("models", [])
                installed_models = [t.get("name") for t in tags]
                # Check direct match or match without tag (e.g., 'llama3.2:latest' -> 'llama3.2')
                if any(self.model in m or m in self.model for m in installed_models):
                    return True

                # Try pulling model
                print(f"Model {self.model} not found locally. Pulling from Ollama...")
                pull_url = f"{self.host}/api/pull"
                pull_response = requests.post(
                    pull_url, json={"name": self.model}, timeout=600
                )
                return pull_response.status_code == 200
            return False
        except Exception as e:
            print(f"Failed to check/pull model {self.model}: {e}")
            return False

    def _extract_metadata_heuristically(self, text: str) -> dict:
        """
        Fallback parser that extracts metadata using rule-based heuristics and regex
        when the local Ollama LLM is unavailable.
        """
        import re

        text_lower = text.lower()

        # 1. Document Type Classification
        invoice_keywords = [
            "invoice",
            "receipt",
            "bill",
            "amount due",
            "total due",
            "payment due",
            "subtotal",
            "tax",
            "gst",
            "vat",
            "invoice number",
            "qty",
            "quantity",
            "billing",
        ]
        resume_keywords = [
            "resume",
            "curriculum vitae",
            "cv",
            "experience",
            "education",
            "skills",
            "projects",
            "employment",
            "professional summary",
            "languages",
            "certification",
            "contact",
            "phone",
            "email",
        ]
        medical_keywords = [
            "patient",
            "blood report",
            "medical",
            "diagnosis",
            "doctor",
            "lab test",
            "hemoglobin",
            "glucose",
            "cholesterol",
            "platelets",
            "clinical",
            "hospital",
            "prescription",
            "urine test",
            "blood test",
        ]
        certificate_keywords = [
            "certificate",
            "certify",
            "awarded to",
            "completion",
            "achievement",
            "participation",
            "certified",
            "presents this",
            "successfully completed",
        ]

        # Score document types
        scores = {
            "Invoice": sum(1 for kw in invoice_keywords if kw in text_lower),
            "Resume": sum(1 for kw in resume_keywords if kw in text_lower),
            "Medical": sum(1 for kw in medical_keywords if kw in text_lower),
            "Certificate": sum(1 for kw in certificate_keywords if kw in text_lower),
        }

        # Determine dominant type
        max_score_type = max(scores, key=lambda k: scores[k])
        doc_type = max_score_type if scores[max_score_type] > 0 else "Notes"

        # 2. Title Extraction
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        title = "Untitled Document"
        if lines:
            first_line = lines[0]
            if len(first_line) < 100:
                title = first_line

        # 3. Tag Extraction
        tags = []
        common_tags = {
            "python": ["python"],
            "javascript": ["javascript", "js"],
            "react": ["react"],
            "sql": ["sql", "sqlite", "mysql", "postgres"],
            "pytorch": ["pytorch"],
            "invoice": ["invoice", "bill", "receipt"],
            "payment": ["payment", "due"],
            "medical": ["medical", "health", "clinical"],
            "blood": ["blood"],
            "certificate": ["certificate", "completion", "award"],
            "notes": ["meeting", "lecture", "memo"],
        }
        for tag_name, synonyms in common_tags.items():
            if any(syn in text_lower for syn in synonyms):
                tags.append(tag_name)

        if not tags:
            tags.append(doc_type.lower())

        # 4. Summary & Specific Metadata Extraction
        summary = f"A local {doc_type} document."
        metadata = {}

        # Regex helpers
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        date_pattern = r"\b(?:\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|\d{2}-\d{2}-\d{4})\b"
        amount_pattern = (
            r"(?:total|amount|due|price|net)[:\s]*(?:\$|rs\.?|€|£)?\s*(\d+(?:\.\d{2})?)"
        )

        if doc_type == "Invoice":
            summary = "An invoice or billing document extracted offline."
            dates = re.findall(date_pattern, text)
            if dates:
                metadata["date"] = dates[0]
            amounts = re.findall(amount_pattern, text_lower)
            if amounts:
                try:
                    float_amounts = [float(a) for a in amounts]
                    metadata["total_amount"] = max(float_amounts)
                except ValueError:
                    pass
            if len(lines) > 0:
                metadata["vendor"] = lines[0]

        elif doc_type == "Resume":
            summary = "A professional resume or CV document parsed offline."
            emails = re.findall(email_pattern, text)
            if emails:
                metadata["contact_email"] = emails[0]
            if len(lines) > 0:
                metadata["applicant_name"] = lines[0]
            skills = [
                t
                for t in tags
                if t in ["python", "javascript", "react", "sql", "pytorch"]
            ]
            if skills:
                metadata["key_skills"] = skills

        elif doc_type == "Medical":
            summary = "A medical report or lab test result analyzed offline."
            dates = re.findall(date_pattern, text)
            if dates:
                metadata["date"] = dates[0]
            patient_match = re.search(
                r"patient\s*(?:name)?[:\s]+([a-zA-Z\s]+)", text, re.IGNORECASE
            )
            if patient_match:
                metadata["patient_name"] = patient_match.group(1).strip()

        elif doc_type == "Certificate":
            summary = "A certificate document recognizing achievement or completion."
            awarded_match = re.search(
                r"(?:awarded|presented)\s+to\s+([a-zA-Z\s]+)", text, re.IGNORECASE
            )
            if awarded_match:
                metadata["recipient"] = awarded_match.group(1).strip()

        else:
            doc_type = "Notes"
            summary = "Personal notes or a general text document."

        return {
            "document_type": doc_type,
            "title": title,
            "tags": tags,
            "summary": summary,
            "metadata": metadata,
        }

    def extract_metadata(self, document_text: str) -> dict:
        """
        Prompt Llama 3.2 to extract structured JSON metadata from the raw text.

        Args:
            document_text (str): The raw text extracted from a PDF or image.

        Returns:
            dict: The structured metadata dictionary matching the specification.
        """
        # Truncate raw text if it's excessively long to prevent CPU/context overload (e.g., limit to ~8000 chars)
        max_chars = 8000
        truncated_text = document_text[:max_chars]
        if len(document_text) > max_chars:
            truncated_text += "\n[Content truncated due to size limitations...]"

        prompt = f"""Analyze the following document text and extract structured information in JSON format.
The JSON object MUST contain the following keys exactly:
- "document_type": A string classifying the document (e.g. "Resume", "Invoice", "Medical", "Certificate", "Notes", "Other").
- "title": A string representing a clean, descriptive title of the document.
- "tags": A list of lowercase strings representing keyword tags (e.g. ["python", "resume", "cv"] or ["invoice", "payment", "utilities"]).
- "summary": A brief 1-2 sentence summary of the document's content.
- "metadata": A dictionary containing key-value pairs representing specific metadata elements extracted from the document. For example:
  - For Invoices: vendor, date, total_amount, tax, billing_address.
  - For Resumes: applicant_name, contact_email, key_skills, years_of_experience.
  - For Medical: patient_name, date, test_type, results.
  - For Certificates: recipient, issuer, issue_date, certificate_name.
  - For Notes/Other: primary_topic, key_points.

Document Text:
---
{truncated_text}
---

Return ONLY the JSON object. Do not include any markdown fences or conversational text.
"""

        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "format": "json",
            "stream": False,
            "options": {
                "temperature": 0.2  # Keep it deterministic
            },
        }

        if not self.check_connection():
            print(
                "Ollama connection failed. Performing local rule-based heuristic extraction."
            )
            heuristics = self._extract_metadata_heuristically(document_text)
            heuristics["summary"] += (
                " (Note: Extracted offline using local heuristic parser; Ollama service was unavailable)"
            )
            return heuristics

        try:
            response = requests.post(
                f"{self.host}/api/generate", json=payload, timeout=90
            )
            if response.status_code == 200:
                result = response.json()
                raw_response = result.get("response", "").strip()
                extracted_json = json.loads(raw_response)

                # Validate schema structure and apply standard defaults
                validated_json = {
                    "document_type": str(
                        extracted_json.get("document_type", "Other")
                    ).capitalize(),
                    "title": str(extracted_json.get("title", "Untitled Document")),
                    "tags": [
                        str(t).lower() for t in extracted_json.get("tags", []) if t
                    ],
                    "summary": str(extracted_json.get("summary", "")),
                    "metadata": dict(extracted_json.get("metadata", {})),
                }
                return validated_json
            else:
                print(
                    f"Ollama API returned status code {response.status_code}. Performing local heuristic extraction."
                )
                return self._extract_metadata_heuristically(document_text)
        except Exception as e:
            print(
                f"Error during Ollama inference: {e}. Performing local heuristic extraction."
            )
            return self._extract_metadata_heuristically(document_text)
