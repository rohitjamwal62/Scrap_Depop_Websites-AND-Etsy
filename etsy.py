'''
for adding time.sleep function
'''
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
header = ["Category","Title","Description","Price","Detail","Rating"]
# driver = webdriver.Chrome('./chromedriver')

options = Options()
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')
# ----------opening esty-----------#


driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get("https://www.etsy.com/")


#----------login into esty-------------#
login = driver.find_element(By.XPATH, 
                            "//button[contains(@class,' wt-btn--small wt-btn--transparent')]"
                            )

login.click()
time.sleep(20)
email = driver.find_element(By.ID, "join_neu_email_field")
email.send_keys('poceho6125@hrisland.com')
password = driver.find_element(By.ID, "join_neu_password_field")
password.send_keys('kindle@123')
submit = email = driver.find_element(By.NAME, "submit_attempt").click()
time.sleep(5)

#--------------search products------------------#
search_prouduts = ['repurposed',"vintage", "reworked"]
# ---------loop for repetition or product search----------]
data = []
for i in search_prouduts:
    search_bar = driver.find_element(By.NAME, "search_query")
    search_bar.clear()

    time.sleep(7)
    search_bar.send_keys(i)
    search_bar.send_keys(Keys.RETURN)

# ----------add filter on product search----------#
    time.sleep(5)
    driver.find_element(By.XPATH, "//*[@id='search-filter-button']").click()
    time.sleep(4)
# ----------shop location--------------#
    shop_location_radio = driver.find_element(By.ID, "shop-location-radio-input")
    driver.execute_script("arguments[0].click();", shop_location_radio)
    shop_location_input = driver.find_element(By.ID, "shop-location-input")
    time.sleep(2)
    shop_location_input.send_keys('United States')

# ----------price filter------------#
    price_radio = driver.find_element(By.ID, "price-input-custom")
    driver.execute_script("arguments[0].click();", price_radio)
    price_input = driver.find_element(By.ID, "search-filter-min-price-input")
    time.sleep(2)
    price_input.send_keys(50)

# ------------item type------------#
    time.sleep(2)
    item_type_handmade= driver.find_element(By.ID, "item-type-input-1")
    driver.execute_script("arguments[0].click();", item_type_handmade)

# -----------ordering option-----------#
    ordering_option_customisable= driver.find_element(By.ID,"customizable")
    driver.execute_script("arguments[0].click();", ordering_option_customisable)
    time.sleep(3)
#------------click on apply------------#
    aplly_filter_button=driver.find_element(By.XPATH, "//*[@id='search-filters-overlay']\
                                            /div/div/div[2]/button[2]")
    driver.execute_script("arguments[0].click();", aplly_filter_button)
    time.sleep(3)

# ------------getting all results products link -----------#
    products_link=[]
    products= driver.find_elements(By.XPATH, "//div/ol/li")
    pagination = driver.find_elements(By.XPATH, "//nav[@aria-label='Review Page Results']/ul/li")
    for element in pagination:
        if element.text == "Next":
            time.sleep(2)
            while True:
                for prd in products:
                    try:
                        products_link.append(prd.find_element(By.TAG_NAME, "a").get_attribute('href')) 
                    except:
                        pass

                time.sleep(5)
                element.click()
                time.sleep(5)
                products = driver.find_elements(By.XPATH,"//div/div/div/ol/li")

# ---------Breaking loop of pagination if there is no next page--------#
                if element.find_element(By.TAG_NAME, "a").get_attribute('disabled')=="true":
                    try:
                        for ele in products:
                            products_link.append(ele.find_element(By.TAG_NAME, "a").get_attribute('href')) 
                    except:
                       continue
                    break

#-----------------scarpping data from each product--------------#
    for link in products_link:
        driver.get(link)
        try:
            price_elements = driver.find_elements(By.XPATH,'//span[@class="currency-value"]')
            for price_element in price_elements:
                price = price_element.text
                price = price.replace(',', '')  # remove commas from the price string
        except:
            price=""
        try:
            name = driver.find_element(By.CSS_SELECTOR, "div[id='listing-page-cart']"
                                    ).find_element(By.TAG_NAME, "h1").text
        except:
            name=""
        try:
            description =  driver.find_element(By.CSS_SELECTOR, "div[id='wt-content-toggle-product-details-read-more']"
                                            ).find_element(By.TAG_NAME, "p").text
        except:
            description=""
        try:
            details =  driver.find_element(By.CSS_SELECTOR, "div[id='product-details-content-toggle']"
                                        ).find_element(By.TAG_NAME, "ul").text
        except:
            details=""
        try:
            rating_span=driver.find_element(By.XPATH, "//a[@href='#reviews']/span/span[2]"
                                            ).find_elements(By.TAG_NAME, "span")
            rating= len(rating_span)
           
        except:
            rating = ""


        All_Records_Here = [i,name,description,price,details,rating]
        with open('new_recods.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(All_Records_Here)
            
print("Suceesssssssssssssssssssssss")