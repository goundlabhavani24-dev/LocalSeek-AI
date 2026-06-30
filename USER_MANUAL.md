# User Manual

# LocalSeek AI

## Overview

LocalSeek AI is an offline document intelligence application that extracts text from PDF and image files, generates AI-powered metadata using Ollama (Llama 3.2), stores information in SQLite, and provides fast local search.

## Requirements

* Python 3.11+
* Ollama
* Llama 3.2
* Tesseract OCR

## Installation

1. Clone the repository.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start Ollama:

```bash
ollama serve
```

4. Verify the model:

```bash
ollama list
```

5. Run the application:

```bash
streamlit run frontend/main.py
```

## Features

* Upload PDF documents
* Upload images
* OCR text extraction
* AI metadata generation
* Local document indexing
* Search documents
* Dashboard statistics
* Offline processing

## Usage

### Upload

Navigate to **Upload**, select a PDF or image, and click **Process Document**.

### Search

Open **Search**, enter keywords, and view matching documents.

### Dashboard

View document statistics and indexed records.

## Troubleshooting

### Ollama not running

Start Ollama:

```bash
ollama serve
```

### Model missing

Download the model:

```bash
ollama pull llama3.2
```

### OCR not working

Ensure Tesseract OCR is installed and available in your system PATH.

## License

Refer to the LICENSE file for licensing information.
