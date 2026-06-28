import json
import requests


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

        payload = {
            "model": self.model,
            "prompt": prompt,
            "format": "json",
            "stream": False,
            "options": {
                "temperature": 0.2  # Keep it deterministic
            },
        }

        fallback_data = {
            "document_type": "Other",
            "title": "Untitled Document",
            "tags": ["unclassified"],
            "summary": "Document content could not be parsed by local LLM.",
            "metadata": {},
        }

        if not self.check_connection():
            print("Ollama connection failed. Returning default metadata.")
            fallback_data["summary"] = (
                "Ollama service is not running locally. Please start Ollama."
            )
            return fallback_data

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
                print(f"Ollama API returned status code {response.status_code}")
                return fallback_data
        except Exception as e:
            print(f"Error during Ollama inference: {e}")
            return fallback_data
