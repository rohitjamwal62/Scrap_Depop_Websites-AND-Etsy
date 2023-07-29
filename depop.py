from selenium import webdriver
from selenium.webdriver.common.by import By
import time,csv,configparser
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

config = configparser.ConfigParser()
config.read('config.ini')
username = config.get('Depop_Creds', 'user')
password = config.get('Depop_Creds', 'password')
First = config.get('Searching_Keywords', 'First')
Second = config.get('Searching_Keywords', 'Second')
Third = config.get('Searching_Keywords', 'Third')
MainList = [First,Second,Third]


options = Options()
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')
# driver = webdriver.Chrome("chromedriver",options=options) # Replace with the path to your chromedriver

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
header = ['Searching_Keyword','Store_Price', 'Product_Rating', 'Here_Next_Url', 'Seller_Name','Last_Active_Date','SoldItem','Rating','Follower','Bio_Detail','Instagram_Link']

driver.maximize_window()
driver.get("https://www.depop.com/login/")
try:
    Click_Cookies = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]").click()
except:
    pass
driver.find_element(By.ID, "username").send_keys(username)
driver.find_element(By.ID, "password").send_keys(password)
try:
    driver.find_element(By.XPATH, "//button[@class='sc-kDDrLX sc-iqcoie sc-cCsOjp jNsXur edBKPF iDnRbj']").click()
except:
    pass
try: 
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)
except:
    pass

driver.get("https://www.depop.com/")

try:
    for keyword in MainList:
        try:
            driver.find_element(By.XPATH, "//button[@id='searchBar__clear-btn']").click()
        except:
            pass
        driver.find_element(By.XPATH, "//input[@name='q']").send_keys(keyword)
        driver.find_element(By.XPATH, "//button[@data-testid='searchBar__submit-btn']").click()
        time.sleep(3)
        GetProducts = driver.find_elements(By.CSS_SELECTOR, "li.imvpaW a")

        Store_all_url_Here = list()
        Empty_list= list()
        SCROLL_PAUSE_TIME = 50
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            time.sleep(10)
            GetProducts = driver.find_elements(By.XPATH, "//a[@data-testid='product__item']")
            driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            for i in GetProducts:
                GetAll_href = i.get_attribute('href')
                Store_all_url_Here.append(GetAll_href) 
            if new_height == last_height:
                print("break")
                break
            last_height = new_height
        for i in Store_all_url_Here:
            if i not in Empty_list:
                Empty_list.append(i)
        time.sleep(2)
        for url in Empty_list:
            All_Records_Here = [url]
            with open('CSV/Url_Backup.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(All_Records_Here)   
                driver.get(url)
                time.sleep(15)
                Next_Url = list()
                try:
                    Product_Rating = driver.find_elements(By.CSS_SELECTOR,"[id*=feedback-star]")[0].text
                except:
                    Product_Rating = "None"
            
                # Price more than 50 filter
                try:
                    data = driver.find_elements(By.XPATH,"//div/p[@aria-label='Price']")[0].text.strip()
                    price = data.split('.')[0]
                    Store_Price = price.split('.')[0][1:len(price)]
                except:
                    Store_Price = 0

    #             # Sales greater than Filter
                try:
                    Sold_Item_Here = driver.find_elements(By.XPATH,"//p[contains(text(),'sold')]")[0].text.strip()
                except:
                    Sold_Item_Here = "None"
                Sold_Item_Here = driver.find_elements(By.XPATH,"//div/p[@class='sc-jqUVSM Signalstyle__StyledText-sc-__sc-1xn3qq3-2 dyzxBA iZxOye']")[0].text.strip()
                First_sold_Item = Sold_Item_Here.split(' ')[0]
                Stored_Href = list()
    #             # if int(Store_Price) > 50 and int(First_sold_Item)>12:
            
                try:
                    if int(First_sold_Item)>12:
                        Description = driver.find_element(By.XPATH,"//div/p[@data-testid='product__description']").text.strip()
                except:
                    Description = "None"
                    spans = driver.find_elements(By.XPATH,"//span/a[@data-testid='avatar']")
                    for span in spans:
                        NextPageUrl = span.get_attribute('href')
                        Next_Url.append(NextPageUrl)
                    Here_Next_Url = Next_Url[0]
                    time.sleep(2)
                    driver.get(Here_Next_Url)
                    time.sleep(11)
                    Store_Sold_Item_Here = list()

                    try:
                        Follower = driver.find_element(By.XPATH,"//button/p[@data-testid='followers__count']").text
                        Followers = driver.find_element(By.XPATH,"//button/p[@data-testid='followers__count']").text
                    except:
                        Follower = 0
                    
                    if 'K' in Follower or 'M' in Follower or 'B' in Follower:
                        Last_work_follower = Follower[-1].strip()
                        if 'K' or 'k' == Last_work_follower:
                            Last_work_follower = 1000
                        elif 'M' or 'm' == Last_work_follower:
                            Last_work_follower = 1000
                        elif 'B' or 'b' == Last_work_follower:
                            Last_work_follower = 1000
                        Follower = int(Follower[0:len(Follower)-1].split('.')[0])+int(Last_work_follower)
                    else:
                        Follower = Follower
    #                 # ===============Calculate Average Price==========================
                    try:
                        Store_Average_Price_Here = list()
                        last_height = driver.execute_script("return document.documentElement.scrollHeight")
                        while True:
                            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                            time.sleep(2)
                            new_height = driver.execute_script("return document.body.scrollHeight")
                            if new_height == last_height:
                                break
                            last_height = new_height
                        LoadButtonClick = driver.find_element(By.XPATH, "//button[@class='sc-gFGZVQ ewexUW']")
                        driver.execute_script("arguments[0].scrollIntoView();", LoadButtonClick)
                        time.sleep(2)
                        LoadButtonClick.click()
                        time.sleep(2)
                        GetPrice = driver.find_elements(By.XPATH, "//p[@aria-label='Price']")
                        for i in GetPrice:
                            GetAll_Price = float(i.text[1:])
                            Store_Average_Price_Here.append(GetAll_Price)
                        prices = [float(el) for el in Store_Average_Price_Here]
                        avg_price = sum(prices) / len(prices)
                        Store_Average_Price = round(avg_price)
                        
                    except:
                        Store_Average_Price = 0
    #                 # ===============End Calculate Average Price==========================

                    if len(str(Follower))>=3:
                        if int(Follower) > 100 and Store_Average_Price > 50:
                            print("Price Average 50 Above")
                            print("At least 100 followers")
                            try:
                                Seller_Name = driver.find_element(By.XPATH,"//div/h1").text
                            except:
                                Seller_Name = "None"
                            time.sleep(1)
                            try:
                                Sold = driver.find_elements(By.XPATH,"//div/div/p[@class='sc-jqUVSM Signalstyle__StyledText-sc-__sc-1xn3qq3-2 dyzxBA iZxOye']")
                            except:
                                pass
                            for Sold_Item in Sold:
                                Get_SoldTest = Sold_Item.text
                                if 'sold' in Get_SoldTest.split(' ')[-1].split():
                                    Sold_Item_Here = Get_SoldTest
                                    Store_Sold_Item_Here.append(Sold_Item_Here)
                            Last_Active_Date = Get_SoldTest
                            if "Active today" or "Active this week" == Last_Active_Date:
                                SoldItem = Store_Sold_Item_Here[0]
                                try:
                                    Rating = driver.find_element(By.XPATH,"//button/p[@data-testid='feedback-btn__total']").text
                                except:
                                    Rating = "None"
                                
                                try:
                                    Bio_Detail =  driver.find_element(By.XPATH,"//div/p[@class='sc-jqUVSM dyzxBA']").text
                                except:
                                    Bio_Detail = "None" 
                                try:
                                    Instagram_Link = driver.find_elements(By.XPATH,"//div/a[@rel='nofollow ugc noreferrer noopener']")[0].text
                                except:
                                    Instagram_Link = "None"
                                All_Records_Here = [keyword,Store_Average_Price,Product_Rating,Here_Next_Url,Seller_Name,Last_Active_Date,SoldItem,Rating,Followers,Bio_Detail,Instagram_Link]
                                with open('new_recods.csv', 'a', encoding='UTF8') as f:
                                    writer = csv.writer(f)
                                    writer.writerow(All_Records_Here)
                else:
                    print("Filter price is less than based upon your requirement.")
except:
    pass
print("Success")
driver.close()