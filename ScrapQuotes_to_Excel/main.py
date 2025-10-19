import requests
from bs4 import BeautifulSoup
import openpyxl

# ---------- Setup Excel ----------
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "love quotes"
sheet.append(["Quote", "Author", "Tags"])

# ---------- Request the page ----------
url = "https://quotes.toscrape.com/tag/love/"
print("Requesting URL:", url)
response = requests.get(url)

# Debug: response status
print("Response status code:", response.status_code)
if response.status_code != 200:
    print("Failed to fetch page. Response headers:", response.headers)
    raise SystemExit("Stopping because the page could not be loaded.")

# Debug: show a small snippet of the raw HTML so you know you're looking at the right page
html = response.text
print("\nHTML snippet (first 500 chars):\n")
print(html[:500].replace("\n", " "))  # replace newlines to keep it compact

# ---------- Parse HTML ----------
soup = BeautifulSoup(html, "html.parser")

# Debug: show the <title> so you confirm you're parsing the right document
page_title = soup.title.string if soup.title else "NO TITLE"
print("\nPage title:", page_title)

# ---------- Find quote blocks ----------
quotes = soup.find_all("div", class_="quote") 
print("Number of quote blocks found:", len(quotes))

# If none found, show top-level HTML sections to help debugging
if len(quotes) == 0:
    print("\nNo quote blocks found. You can inspect the DOM manually or print more HTML.")
    # show the part of the page that usually contains quotes
    container = soup.find("div", class_="container")
    if container:
        print("\nContainer snippet (first 500 chars):\n")
        print(container.prettify()[:500])
    else:
        print("No container with class 'container' found either.")
    # Stop here to avoid writing empty file
    raise SystemExit("No data extracted; stopping.")

# ---------- Inspect the first quote element (prettified) ----------
print("\nPrettified first quote element:\n")
print(quotes[0].prettify())

# ---------- Extract fields from each quote and write to Excel ----------
for i, q in enumerate(quotes, start=1):
    # Debug: show the raw HTML of this quote element on each iteration (small)
    print(f"\n--- Quote #{i} raw HTML (short) ---")
    print(q.prettify()[:400])

    # Extract text, author, tags
    text_elem = q.find("span", class_="text")
    author_elem = q.find("small", class_="author")
    tag_elems = q.find_all("a", class_="tag")

    # More defensive coding: check that elements exist
    quote_text = text_elem.get_text().strip() if text_elem else ""
    author = author_elem.get_text().strip() if author_elem else ""
    tags = [t.get_text().strip() for t in tag_elems] if tag_elems else []

    # Debug prints for extracted values
    print("Extracted quote_text:", repr(quote_text))
    print("Extracted author:", repr(author))
    print("Extracted tags:", tags)

    # Append to Excel
    sheet.append([quote_text, author, ", ".join(tags)])

# ---------- Save the workbook ----------
out_file = "love_quotes.xlsx"
workbook.save(out_file)
print(f"\nDone — saved {len(quotes)} rows to '{out_file}'")
