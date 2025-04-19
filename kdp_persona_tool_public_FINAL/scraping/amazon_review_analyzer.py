
import os
import requests

def get_low_star_reviews(asin, max_reviews=10):
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("API key SerpAPI mancante")

    url = "https://serpapi.com/search.json"
    params = {
        "engine": "amazon_reviews",
        "amazon_domain": "amazon.com",
        "asin": asin,
        "api_key": api_key,
        "review_stars": "1,2,3"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise RuntimeError(f"Errore nella richiesta SerpAPI: {response.status_code}")

    data = response.json()
    reviews = data.get("reviews", [])

    # Estrai solo il contenuto delle recensioni (testo)
    texts = [r.get("body") for r in reviews if r.get("body")]
    return texts[:max_reviews]

def format_reviews_for_prompt(reviews):
    if not reviews:
        return "Nessuna recensione disponibile."
    return "📉 RECENSIONI NEGATIVE DA AMAZON:\n" + "\n\n".join(f"- {r}" for r in reviews)
