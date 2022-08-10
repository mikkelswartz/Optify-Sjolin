
import glob
import os
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

if st.button("Run"):
        with st.spinner("Vent venligst, programmet arbejder."):

        data = pd.DataFrame(columns = ["ordernumber", "orderlink", "created", "total_price"])
       
        # Locate chrome webdrive
        driver = webdriver.Chrome(options=options, service_log_path='selenium.log')

        def wait_for_loading(driver, class_name):
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, class_name))
                )
            except:
                driver.quit()
                print("driver quit: page " + str(driver.current_url) + "to slow to load.")
        # open URL
        driver.get(url)

        st.write(driver.title)

        # type ind email and password to login
        driver.find_element_by_name('username').send_keys(email)
        driver.find_element_by_name('password').send_keys(password + Keys.ENTER)

        # relocate to orders when page is loaded
        wait_for_loading(driver, "sidebar-nav")
        driver.get(url+"/orders")

        
        # wait until order page is loaded
        wait_for_loading(driver, "VueTables__row ")


        ####################### test start
        # orderlink = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/table/tbody/tr[21]/td[1]/a').get_attribute('href')
        # print(orderlink)
        # driver.get(orderlink)

        # driver.implicitly_wait(10)
        # #t_body = driver.find_elements_by_xpath('/html/body/div[1]/div/main/div/div/div[3]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div[1]/table/tbody')
        # time.sleep(1)
        # driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div[3]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[1]/td[7]/div/button[1]').click()
        # time.sleep(1)
        # driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div[3]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[1]/td[7]/div/button[1]').click()

        # driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div[3]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[2]/td[7]/div/button[1]').click()
        # #/html/body/div[1]/div/main/div/div/div[3]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[1]/td[7]/div/button[1]
        # #/html/body/div[1]/div/main/div/div/div[3]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div[1]/table/tbody/tr[2]/td[7]/div/button[1]


        ####################### test end



        # find the total amount of orders --> can be used to now how many pages we need to go throug
        total_orders_line = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[3]/nav/p').text
        total_orders = int(total_orders_line.split(' ')[-2].replace(',',''))

        total_pages = int(total_orders/50)
        total_page_ten = total_pages - total_pages % 10

        break_bool = False
        for i in range(0,total_pages+1):
            #for i in range(0,1): ### --> for testing
            driver.implicitly_wait(10)
            time.sleep(0.2)
            # find all orderlines 
            orderlines = driver.find_elements_by_class_name('VueTables__row ')

            count = 0
            for orderline in orderlines:
                # find creation date
                count += 1
                creation_date = (str(driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[2]/table/tbody/tr['+str(count)+']/td[11]').text)[:-6])
                creation_date = datetime.datetime.strptime(creation_date.replace('-',''),"%d%m%Y").date()

                
                if to_date >= creation_date >= from_date:

                    # extract information from orderline
                    order = orderline.find_element_by_class_name('null')
                    orderlink = order.find_element_by_tag_name('a').get_attribute('href')
                    ordernumber = order.find_element_by_tag_name('a').text


                    # If a specific store is chosen, then only keep those orders
                    if store == '':
                        data.loc[len(data)] = [ordernumber, orderlink, creation_date, None]
                    elif ordernumber[-1] == store:
                            data.loc[len(data)] = [ordernumber, orderlink, creation_date, None]
                elif creation_date < from_date:
                    break_bool = True
                    break
            if break_bool:
                break

            # Go to next page
            if i < total_page_ten: # runs if there is 10 pages to choose from
                next_page_button = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[3]/nav/ul/li[13]')
                next_page_button.click()
            elif i != total_pages: # runs if there is less than 10 pages
                next_page_button = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div[2]/div[2]/div[3]/nav/ul/li[' + str(4 + total_pages%10) +']/a')
                next_page_button.click()
            
            


        # Open all orderlinks and scape the information needed.
        for i in range(0, len(data['ordernumber'])):
            # for i in range(0, 2): ### --> for testing
            # """
            # # Open new tab
            # new_tab_script = "window.open('" + str(orderlinks[i]) + "', '" + str(ordernumbers[i]) + "');"
            # driver.execute_script(new_tab_script)
            # #print(driver.current_url)
            # driver.switch_to.window(ordernumbers[i])
            # #print(driver.current_url)
            # """
            # go to next order URL
            driver.get(data['orderlink'][i])

            # Wait for page to load
            driver.implicitly_wait(10)

            # find total cost
            total_containter = driver.find_element_by_class_name('total')
            total_containter_last = total_containter.find_element_by_class_name('last')
            total_cost = (total_containter_last.find_element_by_class_name('float-right').text)[:-3].replace('.','').replace(',','.')

            data['total_price'][i] = float(total_cost)

        st.write(data[['ordernumber', 'created', 'total_price']])
        st.write("Total turnover:", data['total_price'].sum(), "DKK" )

        #time.sleep(10)
        #close the driver
        driver.quit()
    
