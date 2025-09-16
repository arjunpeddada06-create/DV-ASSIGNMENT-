import streamlit as st
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import string
import io
import json

st.set_page_config(page_title="Text Visualizer", layout="wide")

st.title("📊 Text Data Visualizer")
st.markdown("Upload `.txt`, `.csv`, `.xlsx`, or `.json` file to explore text data visually.")

# -----------------
# Helper functions
# -----------------
def extract_text(file):
    name = file.name.lower()
    if name.endswith('.txt'):
        text = file.read().decode('utf-8')
        return text
    elif name.endswith('.csv'):
        df = pd.read_csv(file)
        return ' '.join(df.astype(str).stack().tolist())
    elif name.endswith('.xlsx'):
        df = pd.read_excel(file)
        return ' '.join(df.astype(str).stack().tolist())
    elif name.endswith('.json'):
        content = json.load(file)
        if isinstance(content, dict):
            return ' '.join(map(str, content.values()))
        elif isinstance(content, list):
            return ' '.join(map(str, content))
    else:
        return None

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud

def get_word_freq(text, n=20):
    words = text.split()
    return Counter(words).most_common(n)

# -----------------
# Upload section
# -----------------
uploaded_file = st.file_uploader("Upload a file", type=['txt', 'csv', 'xlsx', 'json'])

if uploaded_file:
    raw_text = extract_text(uploaded_file)
    if raw_text:
        clean = clean_text(raw_text)

        st.subheader("📈 Text Statistics")
        words = clean.split()
        st.markdown(f"**Total Characters:** {len(clean)}")
        st.markdown(f"**Total Words:** {len(words)}")
        st.markdown(f"**Unique Words:** {len(set(words))}")

        # Word Frequency
        st.subheader("🔢 Most Frequent Words")
        freq_words = get_word_freq(clean)
        df_freq = pd.DataFrame(freq_words, columns=['Word', 'Frequency'])

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(df_freq['Word'], df_freq['Frequency'], color='skyblue')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Word Cloud
        st.subheader("☁️ Word Cloud")
        wc = generate_wordcloud(clean)
        fig_wc, ax_wc = plt.subplots(figsize=(12, 6))
        ax_wc.imshow(wc, interpolation='bilinear')
        ax_wc.axis("off")
        st.pyplot(fig_wc)

    else:
        st.error("Unsupported file or failed to read text.")
else:
    st.info("Please upload a file to begin.")
