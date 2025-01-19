import streamlit as st
import requests
import json

# Function to call the API and get news articles
def fetch_news():
    url = 'YOUR_API_ENDPOINT'  # Replace with your actual API endpoint
    headers = {
        'Content-Type': 'application/json'
    }
    body = {
        "topic": "Women Empowerment"
    }
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        return response.json()
    else:
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
