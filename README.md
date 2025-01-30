# Federal Register Executive Orders Text Extractor

This script downloads executive orders from the Federal Register, extracts their text content, and creates a consolidated JSON file containing both the metadata and full text of each order.

## Description

The main script (`download-and-update-json.py`) performs the following operations:
1. Downloads a JSON file containing metadata about executive orders from the Federal Register API
2. Downloads PDF versions of each executive order
3. Extracts text content from the PDFs
4. Creates a new JSON file that includes both the original metadata and extracted text content
5. Saves individual text files for each executive order

Because there is a delay between signing of an order and publication on the Federal Register, it can be convenient to scrape the orders themselves from another source. [The American Presidency Project](https://www.presidency.ucsb.edu/documents/app-categories/written-presidential-orders/presidential/executive-orders?items_per_page=40&field_docs_start_date_time_value[value][date]=2025) posts all Executive Orders to their website quite rapidly, and has a convenient listing.  `alternative-scraper.py` crawls and scrapes Executive Orders from here, using a simple/ad-hoc JSON schema. The download script is preferred for projects dependent on authoritative data sources; the scraper is useful for timely or urgent analysis and response. It performs the following tasks:
1. Find links to individual EOs
2. Crawl to and parse the individual pages
3. Record results in `documents_scraped.json`

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
├── alternative-scraper.py
├── download-and-update-json.py
├── requirements.txt
├── pdfs/                      # Created during execution
├── texts/                     # Created during execution
└── documents.json             # Created during execution
└── documents_with_text.json   # Created during execution
└── executive_orders_2025.json # Created during execution of scraper
```

## Usage

Run the download script from the command line:

```bash
python download-and-update-json.py
```

Or alternatively run the scraper:
```bash
python alternative-scraper.py
```

## Output

The `download-and-update-json` script creates several directories and files:

- `pdfs/`: Contains downloaded PDF files of executive orders
- `texts/`: Contains extracted text files (one per executive order)
- `documents.json`: Original JSON data from the Federal Register API
- `documents_with_text.json`: Enhanced JSON file including extracted text content

`alternative-scraper.py`, by contrast, creates only the final output file:
- `documents_scraped.json`: simple JSON file recording date, president, title, and text content

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

*TODO*: document error handling in scraper.

## Dependencies

- `requests`: For downloading JSON and PDF files
- `PyPDF2`: For extracting text from PDF files
- `eautifulsoup4`: For scraping content from HTML pages
See `requirements.txt` for specific version requirements.

## Success Metrics

The script provides a summary of:
- Total PDFs processed
- Successfully processed PDFs
- Failed PDFs
- Total pages processed


## Note

The download script is specifically designed to work with the Federal Register API and assumes a specific format for the input JSON data. The target URL is configured to fetch executive orders signed by Donald Trump starting on January 20, 2025.

