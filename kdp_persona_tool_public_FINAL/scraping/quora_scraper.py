
def scrape_quora_answers(keyword):
    print(f"[DEBUG] Simulazione scraping Quora per: {keyword}")
    return [f"Quora answer 1 about {keyword}", f"Quora answer 2 about {keyword}"]

def format_quora_for_prompt(answers):
    return "\n".join(answers)
