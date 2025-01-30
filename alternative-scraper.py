import requests
from bs4 import BeautifulSoup
import json
import time

target_president_re = "Trump"
def get_executive_orders_2025():
    """
    Crawls all Executive Orders published in 2025 from the American Presidency Project,
    following pagination, scraping metadata and the main text, and returns a list of dicts.
    """

    base_url = (
        "https://www.presidency.ucsb.edu/documents/"
        "app-categories/written-presidential-orders/presidential/executive-orders"
    )

    # We'll collect all executive order data here
    all_orders = []
    
    # We start from page=1 and continue until there's no next page link
    page_number = 0
    
    # Items per page (40 in the sample URL)
    items_per_page = 40
    
    # We keep going until no "next" link is found
    while True:
        # Construct the URL for this page
        # page=X is the pagination parameter used by the site
        params = {
            "items_per_page": items_per_page,
            "field_docs_start_date_time_value[value][date]": "2025",
            "page": page_number
        }
        
        print(f"Fetching listing page: {page_number}...")
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print(f"Failed to retrieve page {page_number}. HTTP Status {response.status_code}")
            break
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Each document is typically inside a listing block, e.g. "div.views-row"
        doc_listings = soup.select("div.views-row")
        
        if not doc_listings:
            print("No documents found on this page. Stopping.")
            break
        
        # Parse each listing on the page
        for doc in doc_listings:
            # Often the link to the EO page is in an <a> tag under a title or heading
            title_link = doc.find("a")
            if not title_link:
                continue

            title = title_link.get_text(strip=True)
            url = "https://www.presidency.ucsb.edu" + title_link["href"]
            
            # Now scrape details from the individual page
            order_data = scrape_executive_order_page(url)
            
            # If we successfully got data, add it to our list
            if order_data and (target_president_re  in order_data["president"]):
                # Insert the listing title as well, or keep whichever is more reliable
                order_data["title"] = title
                order_data["url"] = url
                all_orders.append(order_data)
        
        # Check if there's a 'next page' link
        next_link = soup.select_one("li.next a")
        if not next_link:
            print("No next page link found. Finished.")
            break
        
        # Otherwise, increment page_number to continue
        page_number += 1
        
        # Be polite and wait a bit
        time.sleep(1)
        
    return all_orders

def scrape_executive_order_page(url):
    """
    Given the URL to a specific Executive Order page on the site,
    scrape relevant metadata and the text of the order.
    
    This version includes alternative selectors to handle potential changes
    on the presidency.ucsb.edu layout.
    """
    print(f"Scraping EO page: {url}")
    try:
        resp = requests.get(url)
        if resp.status_code != 200:
            print(f"Failed to load {url}. HTTP Status: {resp.status_code}")
            return None
        
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # # Title: Try multiple selectors
        # title_tag = (
        #     soup.select_one("h1.document-title") or
        #     soup.select_one("div.field--name-field-document-title h2") or
        #     soup.select_one("h1.title") or
        #     soup.find("h1")
        # )
        # eo_title = title_tag.get_text(strip=True) if title_tag else None
        
        # Date: might still be in <span class="date-display-single">
        date_tag = soup.find("span", class_="date-display-single")
        # If not, you can add a fallback, e.g.:
        # date_tag = date_tag or soup.select_one("div.field--name-field-doc-date time")
        eo_date = date_tag.get_text(strip=True) if date_tag else None
        
        # President
        president = None
        
        pres_tag = pres_tag = soup.select_one("h3.diet-title a")
        if pres_tag:
            president = pres_tag.get_text(strip=True)
        else:
            # Attempt #3: Fallback - search for a paragraph that might contain the word "President"
            pres_text_candidates = soup.find_all("p")
            for ptag in pres_text_candidates:
                text = ptag.get_text(strip=True)
                if "President" in text:
                    president = text
                    break
        
        # EO text: often in <div class="field-docs-content">
        text_div = soup.find("div", class_="field-docs-content")
        if not text_div:
            # fallback approach
            text_div = soup.select_one("div.field--name-body, div#block-system-main")
        eo_text = text_div.get_text(separator="\n", strip=True) if text_div else None

        
        data = {
            # "title": eo_title,
            "date": eo_date,
            "president": president,
            "text": eo_text,
        }
        return data
    
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

if __name__ == "__main__":
    # Scrape all 2025 Executive Orders
    executive_orders = get_executive_orders_2025()
    
    # Write results to JSON
    with open("documents_scraped.json", "w", encoding="utf-8") as f:
        json.dump(executive_orders, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(executive_orders)} executive orders to executive_orders_2025.json")
