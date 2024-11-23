import requests, os
from scholarly import scholarly

def scrape_google_scholar(query, max_results=10):
    """Search Google Scholar and return articles with downloadable PDFs."""
    search_query = scholarly.search_pubs(query)
    articles = []
    for _ in range(max_results):
        try:
            article = next(search_query)
            if "eprint_url" in article:
                articles.append({
                    "title": article.get("bib", {}).get("title", ""),
                    "abstract": article.get("bib", {}).get("abstract", ""),
                    "authors": article.get("bib", {}).get("author", []),
                    "pub_year": article.get("bib", {}).get("pub_year", ""),
                    "eprint_url": article.get("eprint_url", ""),
                })
        except StopIteration:
            break
    return articles

def download_pdf(url, output_dir, filename):
    """Downloads a PDF from the provided URL."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        os.makedirs(output_dir, exist_ok=True)
        pdf_path = os.path.join(output_dir, filename)
        with open(pdf_path, 'wb') as pdf_file:
            pdf_file.write(response.content)
        return pdf_path
    else:
        raise Exception(f"Failed to download PDF from {url}")
