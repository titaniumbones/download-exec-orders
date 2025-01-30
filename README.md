# Federal Register Executive Orders Text Extractor

This script downloads executive orders from the Federal Register, extracts their text content, and creates a consolidated JSON file containing both the metadata and full text of each order.

## Description

The script performs the following operations:
1. Downloads a JSON file containing metadata about executive orders from the Federal Register API
2. Downloads PDF versions of each executive order
3. Extracts text content from the PDFs
4. Creates a new JSON file that includes both the original metadata and extracted text content
5. Saves individual text files for each executive order

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Clone this repository or download the files
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Project Structure

```
exec-orders/
├── download-and-update-json.py
├── requirements.txt
├── pdfs/                    # Created during execution
├── texts/                   # Created during execution
└── documents.json           # Created during execution
└── documents_with_text.json # Created during execution
```

## Usage

Run the script from the command line:

```bash
python download-and-update-json.py
```

## Output

The script creates several directories and files:

- `pdfs/`: Contains downloaded PDF files of executive orders
- `texts/`: Contains extracted text files (one per executive order)
- `documents.json`: Original JSON data from the Federal Register API
- `documents_with_text.json`: Enhanced JSON file including extracted text content

## File Naming Convention

- PDF files are named using the document number: `{document_number}.pdf`
- Text files are named using both document number and title: `{document_number}_{title}.txt`

## Error Handling

The script includes error handling for:
- Failed JSON downloads
- Failed PDF downloads
- Failed text extraction
- Failed file writing operations

If any individual document fails to process, the script will continue with the remaining documents.

## Dependencies

- `requests`: For downloading JSON and PDF files
- `PyPDF2`: For extracting text from PDF files

See `requirements.txt` for specific version requirements.

## Success Metrics

The script provides a summary of:
- Total PDFs processed
- Successfully processed PDFs
- Failed PDFs
- Total pages processed


## Note

This script is specifically designed to work with the Federal Register API and assumes a specific format for the input JSON data. The target URL is configured to fetch executive orders signed by Donald Trump between January 20, 2025, and January 30, 2025.
