import streamlit as st
import requests
import json
import pandas as pd
from io import BytesIO
import os
from dotenv import load_dotenv


# Configure page
st.set_page_config(
    page_title="Web Scraper Interface",
    page_icon="🌐",
    layout="wide"
)

# Replace this with your Render.com API URL
API_URL = "https://web-scrapper-project-mk3w.onrender.com"

# Get OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Add API key validation
if not OPENAI_API_KEY:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

def main():
    st.title("Web Scraper Interface 🌐")
    st.write("Enter a topic and click the button to start scraping!")

    # Input field for topic
    topic = st.text_input("Enter Topic", "Women Empowerment")

    # Create columns for buttons
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Start Scraping"):
            with st.spinner('Scraping in progress...'):
                try:
                    response = requests.post(
                        f"{API_URL}/scrape",
                        json={"topic": topic},
                        timeout=300  # 5 minutes timeout
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Convert result to DataFrame
                        df = pd.DataFrame(result['result'])
                        
                        # Create Excel file in memory
                        output = BytesIO()
                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                            df.to_excel(writer, index=False)
                        
                        # Provide download button
                        st.download_button(
                            label="Download Results",
                            data=output.getvalue(),
                            file_name=f"{topic}_scraping_results.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                        
                        # Display results in the app
                        st.success("Scraping completed successfully!")
                        st.dataframe(df)
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    with col2:
        if st.button("Train Model"):
            with st.spinner('Training in progress...'):
                try:
                    response = requests.post(
                        f"{API_URL}/train",
                        json={
                            "topic": topic,
                            "n_iterations": 5,
                            "filename": "training_data.json"
                        }
                    )
                    if response.status_code == 200:
                        st.success("Training completed successfully!")
                        st.json(response.json())
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    with col3:
        if st.button("Test Model"):
            with st.spinner('Testing in progress...'):
                try:
                    response = requests.post(
                        f"{API_URL}/test",
                        json={
                            "topic": topic,
                            "n_iterations": 5,
                            "openai_model_name": "gpt-3.5-turbo"
                        }
                    )
                    if response.status_code == 200:
                        st.success("Testing completed successfully!")
                        st.json(response.json())
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    # Add sidebar with additional information
    st.sidebar.title("About")
    st.sidebar.info(
        "This web interface allows you to interact with the Web Scraper API. "
        "Simply enter a topic and click the appropriate button to start the process."
    )

    # Add footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>Created with ❤️ by Your Name</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 
    
