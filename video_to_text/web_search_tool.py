# web_search_tool.py
import requests
from bs4 import BeautifulSoup
import time


class WebSearchTool:
    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        }

    def search_profiles(self, query: str, max_results: int = 5) -> list[str]:
        """
        Search web safely with retry & fallback
        """
        print(f"🔍 Searching web for: {query}")

        try:
            return self._duckduckgo_search(query, max_results)
        except Exception as e:
            print(f"⚠ DuckDuckGo failed: {e}")
            print("🔁 Falling back to Bing-like HTML search")
            results = self._fallback_search(query, max_results)
            print(f"✅ Fallback returned {len(results)} results")
        return results

            

    def _duckduckgo_search(self, query, max_results):
        url = "https://duckduckgo.com/html/"
        params = {"q": query}

        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=10
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        snippets = soup.select(".result__snippet")

        return [
            snippet.get_text(strip=True)
            for snippet in snippets[:max_results]
        ]

    def _fallback_search(self, query, max_results):
        """
        Simple fallback using textise approach
        """
        url = "https://www.bing.com/search"
        params = {"q": query}

        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=10
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        snippets = soup.select("li.b_algo p")

        return [
            snippet.get_text(strip=True)
            for snippet in snippets[:max_results]
        ]
