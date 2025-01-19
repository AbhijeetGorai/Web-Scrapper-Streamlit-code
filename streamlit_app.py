import streamlit as st
import requests
import json

# Function to call the API and get news articles
def fetch_news():
    url = 'https://web-scrapper-project-mk3w.onrender.com/scrape'  # Replace with your actual API endpoint
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

# Function to format the news articles into a text file
def format_news_to_text(news_data):
    articles = news_data.get('articles', [])
    formatted_text = ""
    for article in articles:
        formatted_text += f"Title: {article.get('title', 'No Title')}\n"
        formatted_text += f"Description: {article.get('description', 'No Description')}\n"
        formatted_text += f"URL: {article.get('url', 'No URL')}\n"
        formatted_text += f"Published At: {article.get('publishedAt', 'No Date')}\n"
        formatted_text += "\n"
    return formatted_text

# Streamlit app
st.title("News on Women Empowerment")

if st.button("Fetch News"):
    news_data = fetch_news()
    if news_data:
        formatted_text = format_news_to_text(news_data)
        st.download_button(
            label="Download News Articles",
            data=formatted_text,
            file_name="women_empowerment_news.txt",
            mime="text/plain"
        )
    else:
        st.error("Failed to fetch news articles. Please try again later.")
