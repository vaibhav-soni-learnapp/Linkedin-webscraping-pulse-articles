import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

def download_html(url):
    response = requests.get(url)
    with open("downloaded_page.html", "w") as f:
        f.write(response.text)

def extract_classes(file_path, classes):
    with open(file_path, "r") as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    extracted_data_list = []
    for class_name, class_list in classes.items():
        elements = []
        for single_class in class_list.split('.'):
            if single_class:  # To skip empty strings
                if '[' in single_class and ']' in single_class:
                    # Special handling for class names with square brackets
                    elements.extend([tag for tag in soup.find_all(class_=True) if single_class.replace('[', '\[').replace(']', '\]') in tag['class']])
                else:
                    elements.extend(soup.find_all(class_=single_class))
        for element in elements:
            extracted_data = {}
            extracted_data[class_name] = element.text.strip()
            extracted_data_list.append(extracted_data)
    
    return extracted_data_list

# Streamlit UI
st.title('HTML Scraper and Data Exporter')

default_url = 'https://www.linkedin.com/pulse/topics/business-administration-s50111/product-management-s624/'  # Replace with your default URL
url = st.text_input('Enter URL to scrape:', default_url)
download_button = st.button('Download HTML')

if download_button:
    download_html(url)

    # Define the classes and their labels
    classes_to_extract = {
        'mb_1_class_text': '.mb-1.overflow-hidden.break-words.font-sans.text-lg.font-[500].babybear:text-md',
        'pr_05_pt_05_class_text': '.pr-0.5.pt-0.5',
        'before_middot_pt_05_class_text': '.before:middot.pt-0.5',
        'content_description_class_text': '.content-description.mt-0.5.break-words.font-sans.text-sm.font-normal.babybear:text-xs'
    }

    extracted_data_list = extract_classes("downloaded_page.html", classes_to_extract)
    # Convert list of dictionaries to DataFrame for easier CSV export
    df = pd.DataFrame(extracted_data_list)

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
