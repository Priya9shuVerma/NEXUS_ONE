import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def web_search(query: str, max_results: int = 5):
    url = "https://html.duckduckgo.com/html/"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/140.0.0.0 Safari/537.36"
        )
    }

    response = requests.post(
        url,
        data={"q": query},
        headers=headers,
        timeout=15,
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    for item in soup.select(".result"):
        link_element = item.select_one(".result__a")
        snippet_element = item.select_one(".result__snippet")

        if not link_element:
            continue

        href = link_element.get("href")

        if not href:
            continue

        if href.startswith("/"):
            href = urljoin(url, href)

        # Skip DuckDuckGo ad/redirect URLs
        if "duckduckgo.com/y.js" in href:
            continue

        title = link_element.get_text(" ", strip=True)

        snippet = (
            snippet_element.get_text(" ", strip=True)
            if snippet_element
            else ""
        )

        results.append(
            {
                "title": title,
                "url": href,
                "snippet": snippet,
            }
        )

        if len(results) >= max_results:
            break

    return results
