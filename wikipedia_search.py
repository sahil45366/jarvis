
import requests
import urllib.parse

BASE_URL = "https://en.wikipedia.org/w/api.php"

HEADERS = {
    "User-Agent": "Jarvis-AI-Assistant/1.0"
}


def search_wikipedia(query):

    try:
        query = query.lower().strip()

        remove = [
            "kaun", "tha", "the", "hai", "kya",
            "who", "was", "is", "what",
            "ke baare mein", "batao"
        ]

        for word in remove:
            query = query.replace(word, " ")

        query = " ".join(query.split())

        if not query:
            return None

        # Search for matching Wikipedia pages
        response = requests.get(
            BASE_URL,
            params={
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json",
                "srlimit": 3
            },
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        results = response.json().get(
            "query", {}
        ).get("search", [])

        if not results:
            return None

        # Get the best matching page title
        title = results[0].get("title")

        if not title:
            return None

        # Fetch summary of the selected page
        summary_url = (
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + urllib.parse.quote(title.replace(" ", "_"))
        )

        summary_response = requests.get(
            summary_url,
            headers=HEADERS,
            timeout=10
        )

        summary_response.raise_for_status()

        data = summary_response.json()

        extract = data.get("extract", "").strip()

        if not extract:
            return None

        # Reject ambiguous disambiguation pages
        if data.get("type") == "disambiguation":
            return None

        print("Wikipedia Page:", title)

        return extract[:1000]

    except requests.exceptions.RequestException as e:
        print("Wikipedia Network Error:", e)
        return None

    except Exception as e:
        print("Wikipedia Error:", e)
        return None
