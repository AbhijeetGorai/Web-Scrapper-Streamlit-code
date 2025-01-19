import streamlit as st
import requests
import json

# Function to call the API and get news articles
def fetch_news():
    url = 'https://web-scrapper-project-mk3w.onrender.com/scrape'  # Replace with your actual API endpoint, including the scheme
    headers = {
        'Content-Type': 'application/json'
    }
    body = {
        "topic": "Women Empowerment"
    }
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch news articles: {e}")
        return None

# Function to extract and format the raw text from the JSON response
def extract_raw_text(news_data):
    raw_text = news_data.get('result', {}).get('raw', '')
    return raw_text

# Streamlit app
st.title("News on Women Empowerment")

if st.button("Fetch News"):
    news_data = fetch_news()
    if news_data:
        raw_text = extract_raw_text(news_data)
        st.download_button(
            label="Download News Articles",
            data=raw_text,
            file_name="women_empowerment_news.txt",
            mime="text/plain"
        )
    else:
        st.error("Failed to fetch news articles. Please try again later.")
