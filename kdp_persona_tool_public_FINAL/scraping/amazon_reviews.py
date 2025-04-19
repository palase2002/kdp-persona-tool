
def get_reviews_from_asin(asin, api_key):
    print(f"[DEBUG] Simulazione scraping Amazon ASIN: {asin}")
    return [f"Amazon review 1 for {asin}", f"Amazon review 2 for {asin}"]

def format_reviews_for_prompt(reviews):
    return "\n".join(reviews)
