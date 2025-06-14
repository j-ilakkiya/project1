import streamlit as st
import pandas as pd

# Load data
discourse = pd.read_csv("discourse.csv")
tds = pd.read_csv("tds.csv")

st.set_page_config(page_title="TDS Knowledge Search", layout="wide")
st.title("🔍 TDS Knowledge Base Search")
st.markdown("Search from **Discourse posts** and **TDS content** using a keyword.")

query = st.text_input("Enter your question or keyword")

if query:
    query_lower = query.lower()
    results = []

    # Search in Discourse
    for _, row in discourse.iterrows():
        text = f"{row.get('Title', '')} {row.get('Content', '')}".lower()
        if query_lower in text:
            results.append({
                "source": "Discourse",
                "title": row.get("Title", "")[:100],
                "url": row.get("URL", "")
            })

    # Search in TDS
    for _, row in tds.iterrows():
        text = " ".join(str(x).lower() for x in row.astype(str))
        if query_lower in text:
            results.append({
                "source": "TDS",
                "title": str(row.get("Title", ""))[:100],
                "url": row.get("URL", "")
            })

    if results:
        st.success(f"Found {len(results)} results:")
        for r in results[:10]:
            st.write(f"**[{r['title']}]({r['url']})** — *{r['source']}*")
    else:
        st.error("No results found.")
