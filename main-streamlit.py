

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
import platform

import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-features=VizDisplayCompositor")

#### Locate chrome webdriver
PATH = 'driver/chromedriver'
which_platform = platform.processor()


url = 'https://aarhus.sjolin.dk'

# if local:
if which_platform != '':
    driver = webdriver.Chrome(PATH, options=options)

# if streamlit cloud
else:
    driver = webdriver.Chrome(options=options)
    
url = 'https://aarhus.sjolin.dk'


if __name__ == "__main__":
    
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("Skriv dit brugernavn:")
    with col2:
        password = st.text_input("Skriv din adgangskode:", type="password")

    col1, col2, col3 = st.columns(3)
    with col1:
        from_date = st.date_input("Vælg startdato:")
    with col2:
        to_date = st.date_input("Vælg slutdato:")
    with col3:
        ##### select stores ####
        stores = ["Lyngby (H)", "Århus (M)", "Aalborg (N)"]
        store_container = st.container()
        all_stores = st.checkbox("Vælg alle butikker")
        
        if all_stores:
            selected_stores = store_container.multiselect("Vælg en eller flere butikker:",
                options = stores, default = stores)
        else:
            selected_stores =  store_container.multiselect("Vælg en eller flere butikker:",
                options = stores)
        selected_stores_letter = [x[-2] for x in selected_stores]
        #######################


    ##### Only used when run on localhost ####
    which_platform = platform.processor()
    # if local:
    if which_platform != '':
        import test_variables
        from_date, to_date, username, password = test_variables.get_variables()
    ###########################################



        if st.button("Find omsætning"):
        if len(selected_stores) == 0:
            st.warning("Du skal vælge mindst én butik.")
            
        else:
            with st.spinner("Vent venligst, programmet arbejder."):

                # login to optify
                #login(username, password)
                driver.get(url)

                if driver.current_url != url:
                    # type ind email and password to login
                    driver.find_element(by=By.NAME, value = 'username').send_keys(username)
                    driver.find_element(by=By.NAME, value = 'password').send_keys(password + Keys.ENTER)

                # relocate to orders when page is loaded
                wait_for_loading(driver, "sidebar-nav")
                #time.sleep(0.2)

                #data = iterate_over_order_pages(selected_stores_letter, from_date, to_date)
                #time.sleep(0.2)
                
                #find_turnover(data)

                #driver.quit()
            
    driver.quit()
    
