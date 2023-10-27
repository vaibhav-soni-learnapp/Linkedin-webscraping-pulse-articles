import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import requests

def download_html(url):
    response = requests.get(url)
    with open("downloaded_page.html", "w") as f:
        f.write(response.text)

# Streamlit UI
st.title('HTML Scraper and Data Exporter')

default_url = 'https://www.linkedin.com/pulse/topics/business-administration-s50111/product-management-s624/'  # Replace with your default URL
url = st.text_input('Enter URL to scrape:', default_url)
download_button = st.button('Download HTML')

if download_button:
    download_html(url)

    # Load the HTML file
    with open("downloaded_page.html", 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize empty lists to store the extracted text
    mb_1_text = []
    pr_05_pt_05_text = []
    before_middot_pt_05_text = []
    content_description_text = []

    # Extract the text for each class and append to the respective list
    for tag in soup.find_all(class_='mb-1 overflow-hidden break-words font-sans text-lg font-[500] babybear:text-md'):
        mb_1_text.append(tag.text.strip())

    for tag in soup.find_all(class_='pr-0.5 pt-0.5'):
        pr_05_pt_05_text.append(tag.text.strip())

    for tag in soup.find_all(class_='before:middot pt-0.5'):
        before_middot_pt_05_text.append(tag.text.strip())

    for tag in soup.find_all(class_='content-description mt-0.5 break-words font-sans text-sm font-normal babybear:text-xs'):
        content_description_text.append(tag.text.strip())

    # Align the lengths of all lists to be the same for dataframe creation
    max_len = max(len(mb_1_text), len(pr_05_pt_05_text), len(before_middot_pt_05_text), len(content_description_text))
    mb_1_text = (mb_1_text + [None] * (max_len - len(mb_1_text)))[:max_len]
    pr_05_pt_05_text = (pr_05_pt_05_text + [None] * (max_len - len(pr_05_pt_05_text)))[:max_len]
    before_middot_pt_05_text = (before_middot_pt_05_text + [None] * (max_len - len(before_middot_pt_05_text)))[:max_len]
    content_description_text = (content_description_text + [None] * (max_len - len(content_description_text)))[:max_len]

    # Create a DataFrame from the extracted text
    df = pd.DataFrame({
        'Questions': mb_1_text,
        'Contributions': pr_05_pt_05_text,
        'time': before_middot_pt_05_text,
        'description': content_description_text
    })

    st.dataframe(df)
