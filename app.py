import streamlit as st
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt

# 1. Sentiment Function
def analyze_sentiment(text):
    analysis = TextBlob(str(text))
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# 2. Page Setup
st.set_page_config(page_title="iMDB Sentiment Analyzer", layout="wide")
st.title("🎬 Movie Review Sentiment Analyzer")

# 3. Navigation
choice = st.sidebar.selectbox("Select Mode", ["Single Text", "Bulk CSV Analysis"])

if choice == "Single Text":
    user_input = st.text_area("Write a movie review...")
    if st.button("Analyze"):
        result = analyze_sentiment(user_input)
        st.write(f"Result: {result}")

# --- YAHAN LIKHNA HAI WO CODE ---
else:
    st.subheader("Upload iMDB Dataset (CSV)")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    
    if uploaded_file:
        # File read karna
        df = pd.read_csv(uploaded_file)
        
        # Optimization: Sirf pehli 100 rows pe test karne ke liye niche wali line uncomment karein
        # df = df.head(100) 

        st.success("Dataset loaded successfully!")
        st.write("Preview of Data:", df.head(10)) # Pehli 10 rows dikhayega

        # Column select karne ka option
        col_name = st.selectbox("Text column select karein (iMDB ke liye 'review' select karein)", df.columns)
        
        if st.button("Start Analysis"):
            with st.spinner('Analysing reviews...'):
                df['Result'] = df[col_name].apply(analyze_sentiment)
                
                # Result Graphs
                st.divider()
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(df[[col_name, 'Result']].head(20))
                
                with col2:
                    counts = df['Result'].value_counts()
                    fig, ax = plt.subplots()
                    ax.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=['lightgreen', 'red', 'lightblue'])
                    st.pyplot(fig)
            
            st.download_button("Download Analyzed CSV", df.to_csv(index=False), "imdb_results.csv")