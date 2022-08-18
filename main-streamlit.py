

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

DriverWaitTimer = 30
url = 'https://aarhus.sjolin.dk'

# if local:
if which_platform != '':
    driver = webdriver.Chrome(PATH, options=options)

# if streamlit cloud
else:
    driver = webdriver.Chrome(options=options)
    
url = 'https://aarhus.sjolin.dk'


def wait_for_loading(driver, class_name):
    """ This function is a simpe use of expected_conditions WebDriverWait"""
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )
    except:
        driver.quit()
        print("driver quit: page " + str(driver.current_url) + "to slow to load.")
        

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
                st.write(driver.current_url)
                #time.sleep(0.2)

                #data = iterate_over_order_pages(selected_stores_letter, from_date, to_date)
                #time.sleep(0.2)
                variables = list()
                    
                status = st.info("Danner overblik over ordre.")

                data = pd.DataFrame(columns = ["ordernumber", 
                    "orderlink", 
                    "costumer",
                    "employee",
                    "event",
                    "prod_status",
                    "producer",
                    "order_type",
                    "payment_status",
                    "usage_date",
                    "shipping_date",
                    "created", 
                    "total_price",
                    "total_price_float"])

                # redirect to orders page and wait for loading
                driver.get(url+"/orders")
                #driver.get("https://aarhus.sjolin.dk/orders")
                wait_for_loading(driver, "VueTables__row")

                # find the number of total orders
                total_orders_line = driver.find_element(by=By.CLASS_NAME, value = 'VuePagination__count.VuePagination__count.text-center.col-md-12').text
                total_orders = int(total_orders_line.split(' ')[-2].replace(',',''))

                total_pages = int(total_orders/50)
                break_bool = False
                for i in range(0,total_pages):
                    driver.implicitly_wait(DriverWaitTimer)
                    # find all orderlines 
                    orderlines = driver.find_elements(by=By.CLASS_NAME, value = 'VueTables__row ')

                    count = 0
                    for orderline in orderlines:
                        costumer = employee = event = prod_status = producer = order_type = payment_status = usage_date = shipping_date = None

                        # find creation date
                        count += 1
                        creation_date = (str(driver.find_element(by=By.XPATH, value = '/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/table/tbody/tr['+str(count)+']/td[11]').text)[:-6])
                        creation_date = datetime.datetime.strptime(creation_date.replace('-',''),"%d%m%Y").date()

                        if to_date >= creation_date >= from_date:

                            # extract information from orderline
                            orderline_elements = orderline.find_elements(by=By.CLASS_NAME, value = 'null')
                            orderlink = orderline_elements[0].find_element(by=By.TAG_NAME, value = 'a').get_attribute('href')
                            ordernumber = orderline_elements[0].find_element(by=By.TAG_NAME, value ='a').text

                            if len(variables) != 0:
                                if "costumer" in variables:
                                    costumer = orderline_elements[1].text
                                if "employee" in variables:
                                    employee = orderline_elements[2].text
                                if "event" in variables:
                                    event = orderline.find_element(by=By.CLASS_NAME, value = 'undefined').text
                                if "prod_status" in variables:
                                    prod_status = orderline_elements[3].text
                                if "producer" in variables:
                                    producer = orderline_elements[4].text
                                if "order_type" in variables:
                                    order_type = orderline_elements[5].text
                                if "payment_status" in variables:
                                    payment_status = orderline_elements[6].text
                                if "usage_date" in variables:
                                    usage_date = orderline_elements[7].text
                                if "shipping_date" in variables:
                                    shipping_date = orderline_elements[8].text

                            # If a specific store is chosen, then only keep those orders
                            if ordernumber[-1] in stores:
                                data.loc[len(data)] = [ordernumber, orderlink, costumer, employee, event, prod_status, producer, order_type, payment_status, usage_date, shipping_date, creation_date, None, None]
                        elif creation_date < from_date:
                            break_bool = True
                            break
                    if break_bool:
                        break

                    # Go to next page
                    next_page_button = driver.find_element(by=By.CLASS_NAME, value = 'VuePagination__pagination-item.page-item.VuePagination__pagination-item.VuePagination__pagination-item-next-page.page-item.VuePagination__pagination-item-next-page')
                    next_page_button.click()

                status.empty()

                #find_turnover(data)
                status = st.info("Finder totale pris for hver enkelt ordre:")
                progress_bar = st.progress(0)

                # Open all orderlinks and scape the information needed.
                for i in range(0, len(data['ordernumber'])):

                    # go to next order URL
                    driver.get(data['orderlink'][i])

                    # Wait for page to load
                    driver.implicitly_wait(DriverWaitTimer)

                    # find total cost
                    total_containter = driver.find_element(by=By.CLASS_NAME, value = 'total')
                    total_containter_last = total_containter.find_element(by=By.CLASS_NAME, value = 'last')
                    total_cost = (total_containter_last.find_element(by=By.CLASS_NAME, value = 'float-right').text)[:-3].replace('.','').replace(',','.')

                    data['total_price'][i] = total_cost
                    data['total_price_float'][i] = float(total_cost)

                    progress_bar.progress((1+i)/len(data['ordernumber']))


                progress_bar.empty()
                status.empty()


                st.write(data)

                st.dataframe(data[['ordernumber', 'created', 'total_price']])

                st.write("Total turnover:", "{:.2f}".format(data['total_price_float'].sum()), "DKK" )

                #driver.quit()
            
    driver.quit()
    
