from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import pandas as pd
import datetime
import sys
import streamlit as st

import time
#from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-features=VizDisplayCompositor")

def delete_selenium_log():
    if os.path.exists('selenium.log'):
        os.remove('selenium.log')


def show_selenium_log():
    if os.path.exists('selenium.log'):
        with open('selenium.log') as f:
            content = f.read()
            st.code(content)

def run_selenium():
    name = str()
    with webdriver.Chrome(options=options, service_log_path='selenium.log') as driver:
        url = "https://aarhus.sjolin.dk"
        driver.get(url)
        name = driver.title
    return name

col1, col2 = st.columns(2)

with col1:
    email = st.text_input("Skriv dit brugernavn:")

with col2:
    password = st.text_input("Skriv din adgangskode:", type="password")

col1, col2 = st.columns(2)
with col1:
    from_date = st.date_input("Vælg startdato:")

with col2:
    to_date = st.date_input("Vælg slutdato:")

#store = st.multiselect("Vælg butik: ", options = ["Lyngby (H)", "Århus (M)"])


url = 'https://aarhus.sjolin.dk'
store = "H"
from_date = datetime.date(2022,7,15)
to_date = datetime.date(2022,7,31)
# define email and password
email = ''
#password = ''

if st.button("Run"):
    title = run_selenium()
    
    st.write(title)
    
