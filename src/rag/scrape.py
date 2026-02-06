"""
Web scraper for fetching documentation from URLs.

Fetches HTML pages, extracts main content, converts to markdown,
and saves to data/docs/ for ingestion into ChromaDB.
"""

import argparse
import logging
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

logger = logging.getLogger(__name__)

DOCS_DIR = Path(__file__).parent.parent.parent / "data" / "docs"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}
TIMEOUT = 30


def fetch_page(url: str) -> str:
    """
    Fetch a web page and return the HTML content.

    Args:
        url: The URL to fetch

    Returns:
        The HTML content as a string

    Raises:
        requests.RequestException: If the request fails
    """
    logger.info(f"Fetching {url}")
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()
    return response.text


def extract_main_content(html: str, url: str) -> str:
    """
    Extract the main content from an HTML page.

    Attempts to find the main content area and strips navigation,
    footers, sidebars, and other non-content elements.

    Args:
        html: The HTML content
        url: The source URL (used for site-specific extraction rules)

    Returns:
        The extracted main content as HTML
    """
    soup = BeautifulSoup(html, "html.parser")

    # Site-specific extraction for HashiCorp documentation
    if "developer.hashicorp.com" in url or "hashicorp.com" in url:
        # Try multiple possible content selectors for HashiCorp docs
        main_content = (
            soup.find("main") or
            soup.find("article") or
            soup.find("div", class_="content") or
            soup.find("div", {"role": "main"}) or
            soup.find("div", id="docs-content")
        )
        if main_content:
            return str(main_content)

    # Generic fallback: look for common content containers
    main_content = (
        soup.find("main") or
        soup.find("article") or
        soup.find("div", {"role": "main"}) or
        soup.find("div", class_=re.compile(r"content|main|article|documentation"))
    )

    if main_content:
        return str(main_content)

    # Last resort: return body content
    body = soup.find("body")
    if body:
        return str(body)

    # If nothing found, return the whole thing
    return html


def html_to_markdown(html: str) -> str:
    """
    Convert HTML to markdown.

    Args:
        html: The HTML content

    Returns:
        The markdown content
    """
    # Convert HTML to markdown
    markdown = md(html, heading_style="ATX", bullets="-")

    # Clean up excessive whitespace
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)

    return markdown.strip()


def generate_filename(url: str) -> str:
    """
    Generate a clean filename from a URL.

    Args:
        url: The source URL

    Returns:
        A safe filename (without extension)
    """
    parsed = urlparse(url)
    path = parsed.path.strip("/")

    # Replace slashes with underscores
    filename = path.replace("/", "_")

    # Remove or replace unsafe characters
    filename = re.sub(r"[^\w\-_]", "_", filename)

    # Remove consecutive underscores
    filename = re.sub(r"_+", "_", filename)

    # Trim and ensure it's not too long
    filename = filename.strip("_")[:100]

    # Fallback if empty
    if not filename:
        filename = "page"

    return filename


def scrape_url(url: str, product: str, output_dir: Path) -> Path | None:
    """
    Scrape a single URL and save as markdown.

    Args:
        url: The URL to scrape
        product: The product tag (e.g., "vault", "terraform")
        output_dir: The directory to save the file

    Returns:
        The path to the saved file, or None if failed
    """
    try:
        html = fetch_page(url)
        main_content = extract_main_content(html, url)
        markdown = html_to_markdown(main_content)

        if not markdown or len(markdown) < 100:
            logger.warning(f"Extracted content is too short ({len(markdown)} chars), skipping: {url}")
            return None

        filename = generate_filename(url) + ".md"
        filepath = output_dir / filename

        # Add a header with the source URL
        markdown_with_source = f"# Source: {url}\n\n{markdown}"

        filepath.write_text(markdown_with_source, encoding="utf-8")
        logger.info(f"Saved to {filepath} ({len(markdown)} chars)")

        return filepath

    except requests.RequestException as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to process {url}: {e}")
        return None


def scrape_urls_from_file(urls_file: Path, product: str, auto_ingest: bool = True) -> int:
    """
    Scrape all URLs from a file and save to data/docs/{product}/.

    Args:
        urls_file: Path to a file with one URL per line
        product: The product tag (e.g., "vault", "terraform")
        auto_ingest: Whether to automatically run ingestion after scraping

    Returns:
        The number of successfully scraped pages
    """
    if not urls_file.exists():
        logger.error(f"URLs file not found: {urls_file}")
        return 0

    # Read URLs
    urls = [line.strip() for line in urls_file.read_text().splitlines() if line.strip() and not line.startswith("#")]

    if not urls:
        logger.warning(f"No URLs found in {urls_file}")
        return 0

    logger.info(f"Found {len(urls)} URLs to scrape")

    # Create output directory
    output_dir = DOCS_DIR / product
    output_dir.mkdir(parents=True, exist_ok=True)

    # Scrape each URL
    success_count = 0
    for i, url in enumerate(urls, 1):
        logger.info(f"[{i}/{len(urls)}] Processing {url}")
        if scrape_url(url, product, output_dir):
            success_count += 1

    logger.info(f"Successfully scraped {success_count}/{len(urls)} pages")

    # Auto-ingest if requested
    if auto_ingest and success_count > 0:
        logger.info("Running ingestion pipeline...")
        from src.rag.ingest import ingest_all_docs
        total_chunks = ingest_all_docs()
        logger.info(f"Ingestion complete: {total_chunks} chunks indexed")

    return success_count


def main():
    """CLI entry point for the scraper."""
    from src.config import setup_logging
    setup_logging()

    parser = argparse.ArgumentParser(
        description="Scrape documentation from URLs and ingest into the RAG system."
    )
    parser.add_argument(
        "--urls",
        required=True,
        help="Path to a file with one URL per line",
    )
    parser.add_argument(
        "--product",
        required=True,
        choices=["vault", "terraform", "consul"],
        help="Product tag for the documentation",
    )
    parser.add_argument(
        "--no-ingest",
        action="store_true",
        help="Skip automatic ingestion after scraping",
    )

    args = parser.parse_args()

    urls_file = Path(args.urls)
    auto_ingest = not args.no_ingest

    success_count = scrape_urls_from_file(urls_file, args.product, auto_ingest)

    if success_count == 0:
        print("\nNo pages were successfully scraped. Check the logs for errors.")
        sys.exit(1)

    print(f"\nSuccessfully scraped {success_count} pages.")
    if auto_ingest:
        print("Documentation has been indexed and is ready for search.")
    else:
        print(f"Files saved to data/docs/{args.product}/")
        print("Run 'python -m src.rag.ingest' to index them.")


if __name__ == "__main__":
    main()
