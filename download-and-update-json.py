import json
import os
import requests
import PyPDF2
from urllib.parse import urlparse
from pathlib import Path
import re

def download_json(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to download JSON from URL: {str(e)}")
        return None

def sanitize_filename(filename):
    # Remove or replace invalid characters in filename
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def download_pdf(url, output_path):
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Failed to download {url}: {str(e)}")
        return False

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)

            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

            # Clean up the text: remove extra whitespace and line breaks
            text = ' '.join(text.split())

            return text, num_pages
    except Exception as e:
        print(f"Failed to extract text from {pdf_path}: {str(e)}")
        return None, 0

def process_documents(json_data):
    # Create directories if they don't exist
    pdf_dir = Path("pdfs")
    text_dir = Path("texts")
    pdf_dir.mkdir(exist_ok=True)
    text_dir.mkdir(exist_ok=True)

    total_pdfs = len(json_data['results'])
    successful_pdfs = 0
    failed_pdfs = 0
    total_pages = 0

    # Process each document
    for doc in json_data['results']:
        pdf_url = doc['pdf_url']
        document_number = doc['document_number']
        title = doc['title']

        # Create filenames
        pdf_filename = f"{document_number}.pdf"
        text_filename = sanitize_filename(f"{document_number}_{title}.txt")

        pdf_path = pdf_dir / pdf_filename
        text_path = text_dir / text_filename

        print(f"\nProcessing {pdf_filename}...")

        # Download PDF
        if download_pdf(pdf_url, pdf_path):
            # Extract text
            text, num_pages = extract_text_from_pdf(pdf_path)

            if text is not None:
                # Add text content to JSON
                doc['text_content'] = text

                # Write text to file
                try:
                    with open(text_path, 'w', encoding='utf-8') as f:
                        f.write(text)
                    print(f"Successfully processed {pdf_filename} ({num_pages} pages)")
                    successful_pdfs += 1
                    total_pages += num_pages
                except Exception as e:
                    print(f"Failed to write text file {text_filename}: {str(e)}")
                    failed_pdfs += 1
            else:
                doc['text_content'] = ""  # Empty string for failed extractions
                failed_pdfs += 1
        else:
            doc['text_content'] = ""  # Empty string for failed downloads
            failed_pdfs += 1

    # Print summary
    print("\nProcessing Summary:")
    print(f"Total PDFs: {total_pdfs}")
    print(f"Successfully processed: {successful_pdfs}")
    print(f"Failed to process: {failed_pdfs}")
    print(f"Total pages processed: {total_pages}")

    return json_data

def main():
    # URL for the JSON data
    json_url ="https://www.federalregister.gov/api/v1/documents.json?conditions%5Bcorrection%5D=0&conditions%5Bpresident%5D=donald-trump&conditions%5Bpresidential_document_type%5D=executive_order&conditions%5Bsigning_date%5D%5Bgte%5D=01%2F20%2F2025&conditions%5Bsigning_date%5D%5Blte%5D=01%2F30%2F2025&conditions%5Btype%5D%5B%5D=PRESDOCU&fields%5B%5D=citation&fields%5B%5D=document_number&fields%5B%5D=end_page&fields%5B%5D=html_url&fields%5B%5D=pdf_url&fields%5B%5D=type&fields%5B%5D=subtype&fields%5B%5D=publication_date&fields%5B%5D=signing_date&fields%5B%5D=start_page&fields%5B%5D=title&fields%5B%5D=disposition_notes&fields%5B%5D=executive_order_number&fields%5B%5D=not_received_for_publication&fields%5B%5D=full_text_xml_url&fields%5B%5D=body_html_url&fields%5B%5D=json_url&include_pre_1994_docs=true&maximum_per_page=10000&order=executive_order&per_page=10000"

    try:
        # Download JSON data
        print("Downloading JSON data...")
        json_data = download_json(json_url)

        if json_data is None:
            print("Failed to download JSON data. Exiting...")
            return

        # Save the original downloaded JSON
        output_dir = Path("exec-orders")
        output_dir.mkdir(exist_ok=True)

        original_json_path = output_dir / 'documents.json'
        with open(original_json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"Original JSON saved to {original_json_path}")

        # Process documents and get updated JSON
        updated_json = process_documents(json_data)

        # Save updated JSON with text content
        output_json_path = output_dir / 'documents_with_text.json'
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(updated_json, f, ensure_ascii=False, indent=2)

        print(f"\nUpdated JSON saved to {output_json_path}")

    except Exception as e:
        print(f"Failed to process: {str(e)}")

if __name__ == "__main__":
    main()
