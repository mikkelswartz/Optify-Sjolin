

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
#options.add_argument("--no-sandbox")
#options.add_argument("--disable-extensions")
#options.add_argument("--disable-dev-shm-usage")
#options.add_argument("--disable-gpu")
#options.add_argument("--disable-features=NetworkService")
#options.add_argument("--window-size=1920x1080")
#options.add_argument("--disable-features=VizDisplayCompositor")



if __name__ == "__main__":
    
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
    #email = ''
    #password = ''
    timer = 30

    if st.button("Run"):
        with st.spinner("Vent venligst, programmet arbejder."):

            data = pd.DataFrame(columns = ["ordernumber", "orderlink", "created", "total_price"])

            # Locate chrome webdrive
            #driver = webdriver.Chrome(options=options)
            with webdriver.Chrome(options=options) as driver:

                def wait_for_loading(driver, class_name):
                    try:
                        WebDriverWait(driver, timer).until(
                            EC.presence_of_element_located((By.CLASS_NAME, class_name))
                        )
                    except:
                        driver.quit()
                        print("driver quit: page " + str(driver.current_url) + "to slow to load.")
                # open URL
                driver.get(url)
                time.sleep(5)
                st.write(driver.current_url)

                st.write(driver.title)

                # type ind email and password to login
                #driver.find_element_by_name('username').send_keys(email)
                driver.find_element(by=By.NAME, value = 'username').send_keys(email)
                #driver.find_element_by_name('password').send_keys(password + Keys.ENTER)
                driver.find_element(by=By.NAME, value = 'password').send_keys(password + Keys.ENTER)


                # relocate to orders when page is loaded
                wait_for_loading(driver, "sidebar-nav")
                #WebDriverWait(driver, 10).until(lambda x: x.find_element(by=By.CLASS_NAME, value="sidebar-nav"))
                #driver.implicitly_wait(timer)
                #time.sleep(5)
                #driver.get("https://google.com")
                #time.sleep(5)
                st.write(driver.current_url)

                driver.get(url+"/orders")
                time.sleep(5)
                st.write(driver.current_url)

                # wait until order page is loaded
                wait_for_loading(driver, "VueTables__row")
                #driver.implicitly_wait(timer)
                st.write(driver.current_url)

                total_orders_line = driver.find_element(by=By.CLASS_NAME, value = 'VuePagination__count.VuePagination__count.text-center.col-md-12').text
                total_orders = int(total_orders_line.split(' ')[-2].replace(',',''))
                st.write(total_orders)

                #time.sleep(10)
                #close the driver
                driver.quit()
    
