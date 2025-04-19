import streamlit as st
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
SERPAPI_API_KEY = st.secrets["SERPAPI_API_KEY"]

import streamlit as st
st.set_page_config(page_title="Buyer Persona Tool", layout="centered")
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

# TAB 1 - Buyer Persona
def ask_gpt_for_persona(keyword, asin):
    prompt = f"""
Analizza le recensioni e discussioni online sulla keyword "{keyword}" (libro con ASIN {asin}) e crea una buyer persona dettagliata. Includi:

- Età, genere, professione
- Obiettivi principali
- Frustrazioni/paure
- Dove si informa
- Comportamento d'acquisto
- Linguaggio usato

Simula i dati se le fonti sono indisponibili.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1500
    )
    return response.choices[0].message.content

# TAB 2 - Analisi Recensioni Negative
def get_low_star_analysis(asin):
    prompt = f"""
Hai raccolto le recensioni a 1–3 stelle per il libro con ASIN {asin}. Analizzale e crea un report dei punti dolenti principali. Offri suggerimenti per migliorare un libro concorrente su questa base.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content

# TAB 3 - Generatore Libro Perfetto
def genera_libro(keyword, frustrazioni):
    prompt = f"""
Sei un copywriter esperto in libri per Amazon.

Crea un'idea editoriale perfetta per un libro con la keyword: "{keyword}".

Considera queste frustrazioni ricorrenti dei lettori:
{frustrazioni}

Restituisci:
1. Titolo persuasivo ottimizzato per Amazon
2. Sottotitolo con benefici chiari
3. Indice con 6 capitoli, ognuno con 2–3 sottosezioni
4. Prompt per generare una descrizione coinvolgente con GPT
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.75,
        max_tokens=1200
    )
    return response.choices[0].message.content

def genera_descrizione(keyword):
    prompt_descrizione = f"""
#DESCRIPTION TITLE#

Crea una descrizione Amazon per un libro con keyword: '{keyword3}'.

Informazioni sul lettore ideale:
- Buyer Persona generata (profilo '{keyword1}', ASIN: {asin1})
- Frustrazioni tratte dalle recensioni: {frustrazioni3}

La descrizione deve essere suddivisa in 4 blocchi:

# BLOCCO 1: Testata + Domande chiave per attirare attenzione
# BLOCCO 2: Frustrazioni + Empatia + Soluzione promessa
# BLOCCO 3: Bullet point con benefici e bonus
# BLOCCO 4: Sogno finale + Call to Action

Formato leggibile, con spazi tra i blocchi. Usa **grassetto** per evidenziare le parole chiave.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_descrizione}],
        temperature=0.75,
        max_tokens=1000
    )
    return response.choices[0].message.content


import datetime

def salva_testo(nome_file_base, testo):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_file = f"{nome_file_base}_{timestamp}.txt"
    with open(nome_file, "w", encoding="utf-8") as f:
        f.write(testo)
    return nome_file



import base64

def download_button(label, text, filename):
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{label}</a>'
    st.markdown(href, unsafe_allow_html=True)



import io

def download_streamlit_button(label, text, filename):
    st.download_button(
        label=label,
        data=io.StringIO(text),
        file_name=filename,
        mime="text/plain"
    )



# 🔁 Pulsante per svuotare la sessione
if st.sidebar.button("🧹 Svuota Tutto"):
    for chiave in st.session_state.keys():
        del st.session_state[chiave]
    st.experimental_rerun()


# UI principale
st.title("📚 Buyer Persona & Libro Perfetto Generator")

tab1, tab2, tab3 = st.tabs(["🧠 Buyer Persona", "🔎 Analisi Recensioni", "📘 Generatore Libro Perfetto"])

with tab1:
    st.subheader("🧠 Genera Buyer Persona")
    keyword1 = st.text_input("Keyword libro", "thyroid cookbook")
    asin1 = st.text_input("ASIN libro competitor", "B09XYZ1234")
    if st.button("🔍 Genera Buyer Persona"):
        with st.spinner("Generazione in corso..."):
            try:
                result = ask_gpt_for_persona(keyword1, asin1)
                st.success("✅ Profilo generato!")
                st.text_area("📋 Profilo Persona", result, height=500)
            except Exception as e:
                st.error(f"Errore: {e}")

with tab2:
    st.subheader("🔎 Analizza Recensioni Negative")
    asin2 = st.text_input("ASIN da analizzare", "B09XYZ1234")
    if st.button("🧠 Analizza Recensioni"):
        with st.spinner("Analisi recensioni..."):
            try:
                result = get_low_star_analysis(asin2)
                st.success("✅ Analisi completata!")
                st.text_area("📉 Report recensioni", result, height=500)
            except Exception as e:
                st.error(f"Errore: {e}")

with tab3:
    st.subheader("📘 Generatore Libro Perfetto")
    col1, col2 = st.columns(2)
    with col1:
        keyword3 = st.text_input("📚 Keyword del libro", "menopause cookbook")
    with col2:
        frustrazioni3 = st.text_area("😤 Frustrazioni lette nelle recensioni", 
            """- Ricette complicate
- Ingredienti difficili
- Mancano immagini
- Poche opzioni vegetariane""", height=150)

    

    
    if st.button("📝 Crea Titolo e Sottotitolo in stile Copy"):
        with st.spinner("Generazione in corso..."):
            try:
                prompt = f"Crea un titolo altamente persuasivo e un sottotitolo efficace per un libro con la keyword: '{keyword3}'."
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=300
                )
                titolo_output = response.choices[0].message.content
                st.text_area("📘 Titolo + Sottotitolo", titolo_output, height=200)
                download_streamlit_button("⬇️ Scarica Titolo e Sottotitolo", titolo_output, "titolo_sottotitolo.txt")
            except Exception as e:
                st.error(f"Errore: {e}")

    if st.button("📑 Crea solo Indice del libro"):
        with st.spinner("Generazione indice..."):
            try:
                prompt = f"Scrivi solo l'indice completo per un libro con la keyword: '{keyword3}', con 6 capitoli e 2–3 sottosezioni ciascuno."
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.75,
                    max_tokens=800
                )
                indice_output = response.choices[0].message.content
                st.text_area("📄 Indice del Libro", indice_output, height=400)
                download_streamlit_button("⬇️ Scarica Indice", indice_output, "indice_libro.txt")
            except Exception as e:
                st.error(f"Errore: {e}")

    if st.button("📄 Genera Descrizione Amazon"):
        with st.spinner("Descrizione in corso..."):
            try:
                descrizione = genera_descrizione(keyword3)
                st.success("✅ Descrizione pronta!")
                st.text_area("🛍️ Descrizione Amazon", descrizione, height=500)
                salva_testo("descrizione_amazon", descrizione)
                st.info("📁 Salvato anche in descrizione_amazon_*.txt")
                download_streamlit_button("⬇️ Scarica Descrizione Amazon", descrizione, "descrizione_amazon.txt")
            except Exception as e:
                st.error(f"Errore: {e}")