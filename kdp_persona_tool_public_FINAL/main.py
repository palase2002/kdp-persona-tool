
import os
import argparse
from openai import OpenAI
from datetime import datetime

from scraping.reddit_scraper import search_reddit_posts, format_posts_for_prompt
from scraping.amazon_reviews import get_reviews_from_asin, format_reviews_for_prompt
from scraping.quora_scraper import scrape_quora_answers, format_quora_for_prompt
from output.pdf_generator import generate_pdf
from output.csv_generator import estrai_campi_da_testo, salva_csv

# API keys direttamente nel codice
OPENAI_API_KEY = "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"
SERPAPI_KEY = "c4a25bc1afd484014cb13672f88adf805b5cf506ceb7e428cc5cd1202307cc79"

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_gpt_for_persona(keyword, asin, use_amazon=True, use_reddit=True, use_quora=True):
    sections = []

    if use_amazon:
        amazon_reviews = get_reviews_from_asin(asin, SERPAPI_KEY)
        amazon_text = format_reviews_for_prompt(amazon_reviews)
        sections.append(amazon_text)

    if use_reddit:
        reddit_posts = search_reddit_posts(keyword)
        reddit_text = format_posts_for_prompt(reddit_posts)
        sections.append(reddit_text)

    if use_quora:
        quora_data = scrape_quora_answers(keyword)
        quora_text = format_quora_for_prompt(quora_data)
        sections.append(quora_text)

    prompt = f"""
    Analizza i seguenti dati provenienti da Amazon, Reddit e Quora per la keyword: "{keyword}".
    Crea una buyer persona dettagliata con:
    - Età, genere, professione
    - Obiettivi principali
    - Frustrazioni/paure
    - Dove si informa
    - Comportamento d'acquisto
    - Linguaggio target

    {'\n\n'.join(sections)}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1800
    )

    return response.choices[0].message.content

def salva_output(persona_text, keyword):
    data_ora = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_file = f"output/persona_{keyword.replace(' ', '_')}_{data_ora}.txt"
    os.makedirs("output", exist_ok=True)
    with open(nome_file, "w", encoding="utf-8") as f:
        f.write(persona_text)
    print(f"✅ Buyer Persona salvata in: {nome_file}")
    return nome_file

def main():
    parser = argparse.ArgumentParser(description="Buyer Persona Generator CLI")
    parser.add_argument("--keyword", type=str, help="Keyword del libro (es. thyroid cookbook)")
    parser.add_argument("--asin", type=str, help="ASIN del libro su Amazon")
    parser.add_argument("--no-amazon", action="store_true", help="Disattiva scraping Amazon")
    parser.add_argument("--no-reddit", action="store_true", help="Disattiva scraping Reddit")
    parser.add_argument("--no-quora", action="store_true", help="Disattiva scraping Quora")

    args = parser.parse_args()

    keyword = args.keyword or input("🔤 Inserisci la keyword del tuo libro: ").strip()
    asin = args.asin or input("🔎 Inserisci l'ASIN del libro target: ").strip()

    print("\n⚙️  Generazione buyer persona in corso...")
    persona = ask_gpt_for_persona(
        keyword,
        asin,
        use_amazon=not args.no_amazon,
        use_reddit=not args.no_reddit,
        use_quora=not args.no_quora
    )

    print("\n📋 Profilo generato:\n")
    print(persona)

    salva_output(persona, keyword)
    generate_pdf(persona, keyword)
    campi = estrai_campi_da_testo(persona)
    salva_csv(campi, keyword)

if __name__ == "__main__":
    main()
