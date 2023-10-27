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

    # Create a DataFrame from the extracted text
    df = pd.DataFrame({
        'mb_1_class_text': mb_1_text,
        'pr_05_pt_05_class_text': pr_05_pt_05_text,
        'before_middot_pt_05_class_text': before_middot_pt_05_text,
        'content_description_class_text': content_description_text
    })

    # Align the lengths of all lists to be the same for dataframe creation
    max_len = max(len(mb_1_text), len(pr_05_pt_05_text), len(before_middot_pt_05_text), len(content_description_text))
    for key, value in df.items():
        df[key] = (value.tolist() + [None] * (max_len - len(value)))[:max_len]

    st.table(df)

    csv_export = st.button('Export to CSV')
    if csv_export:
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Download CSV",
            data=csv_buffer,
            file_name="extracted_data.csv",
            mime="text/csv"
        )
