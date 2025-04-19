
import streamlit as st
from scraping.amazon_review_analyzer import get_low_star_reviews
from openai import OpenAI

OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)

def analizza_recensioni_gpt(asin):
    reviews = get_low_star_reviews(asin)
    review_list_text = "\n- " + "\n- ".join(reviews)

    prompt = f"""
Analizza queste recensioni negative (1–3 stelle) di un libro:

{review_list_text}

📌 Crea un report con:
1. I problemi principali evidenziati dai lettori
2. Le mancanze ricorrenti
3. Come migliorare un libro concorrente in base a queste recensioni

Scrivi in modo chiaro, come fosse una consulenza editoriale.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content

# Aggiunta sezione nella GUI
st.header("🔍 Analisi delle Recensioni (1–3 stelle)")

asin_input = st.text_input("Inserisci l'ASIN del libro concorrente da analizzare:", "B0CGLWYYXK")

if st.button("🧠 Analizza Recensioni Negativi"):
    with st.spinner("Analisi in corso con GPT..."):
        try:
            output = analizza_recensioni_gpt(asin_input)
            st.success("✅ Analisi completata!")
            st.text_area("📋 Report", output, height=400)
        except Exception as e:
            st.error(f"Errore durante l'analisi: {e}")
