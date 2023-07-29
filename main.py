from selenium import webdriver
from selenium.webdriver.common.by import By
import time,csv
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


options = Options()
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.maximize_window()
file_path = 'No_Duplicate_Records_CSV/New_vintage.csv'
empty_list= list()

with open(file_path, 'r') as file:
    reader = csv.reader(file)
    for GetUrl in reader:
        for url in GetUrl:
            driver.get(url)
            try:
                
                Click_Cookies = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]").click()
            except:
                pass
            time.sleep(1)
            # Start Code Here_________________
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
            # Sales greater than Filter
            try:
                Sold_Item_Here = driver.find_elements(By.XPATH,"//p[contains(text(),'sold')]")[0].text.strip()
            except:
                Sold_Item_Here = "None"

            Description_List = list()
            First_sold_Item_List = list()
            try:
                Sold_Item_Here = driver.find_elements(By.XPATH,"//div/p[contains(text(),'sold')]")
                for sold_Price in Sold_Item_Here:
                    First_sold_Item = sold_Price.text.strip().split(' ')[0]
                    First_sold_Item_List.append(First_sold_Item)
                    # if int(Store_Price) > 5 and int(First_sold_Item)>12:
                    try:
                        if int(First_sold_Item)>12:
                            Description = driver.find_element(By.XPATH,"//div/p[@data-testid='product__description']").text.strip()
                            Description_List.append(Description)
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
                    # print("Checking......................")
                    Store_Average_Price_Here = list()
                    last_height = driver.execute_script("return document.documentElement.scrollHeight")
                    while True:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)
                        new_height = driver.execute_script("return document.body.scrollHeight")
                        if new_height == last_height:
                            break
                        last_height = new_height
                    LoadButtonClick = driver.find_element(By.XPATH, "//button[contains(., 'Load more')]")
                    driver.execute_script("arguments[0].scrollIntoView();", LoadButtonClick)
                    time.sleep(2)
                    LoadButtonClick.click()




                    
                    print("yesssssss")
                    print("Work here below-------------")
                    time.sleep(2)
                    GetPrice = driver.find_elements(By.XPATH, "//p[@aria-label='Price']")
                    print(GetPrice,"______________")
                    # for i in GetPrice:
                    #     print(i,"__________________")
                    #     GetAll_Price = float(i.text[1:])
                    #     Store_Average_Price_Here.append(GetAll_Price)
                    # prices = [float(el) for el in Store_Average_Price_Here]
                    # avg_price = sum(prices) / len(prices)
                    # Store_Average_Price = round(avg_price)
                    # print(Store_Average_Price)
                    
                except:
                    Store_Average_Price = 0
                payload = [Follower,First_sold_Item_List,Description_List,Product_Rating,Store_Price,Store_Average_Price]
                



                # # ===============End Calculate Average Price==========================

                # if len(str(Follower))>=3:
                  
                #     if int(Follower) > 100 and Store_Average_Price > 5:
                #         print("Price Average 50 Above")
                #         print("At least 100 followers")
                #         try:
                #             Seller_Name = driver.find_element(By.XPATH,"//div/h1").text
                #         except:
                #             Seller_Name = "None"
                #         time.sleep(1)
                #         try:
                #             Sold = driver.find_elements(By.XPATH,"//div/div/p[@class='sc-jqUVSM Signalstyle__StyledText-sc-__sc-1xn3qq3-2 dyzxBA iZxOye']")
                #         except:
                #             pass
                #         for Sold_Item in Sold:
                #             Get_SoldTest = Sold_Item.text
                #             if 'sold' in Get_SoldTest.split(' ')[-1].split():
                #                 Sold_Item_Here = Get_SoldTest
                #                 Store_Sold_Item_Here.append(Sold_Item_Here)
                #         Last_Active_Date = Get_SoldTest
                #         if "Active today" or "Active this week" == Last_Active_Date:
                #             SoldItem = Store_Sold_Item_Here[0]
                #             try:
                #                 Rating = driver.find_element(By.XPATH,"//button/p[@data-testid='feedback-btn__total']").text
                #             except:
                #                 Rating = "None"
                            
                #             try:
                #                 Bio_Detail =  driver.find_element(By.XPATH,"//div/p[@class='sc-jqUVSM dyzxBA']").text
                #             except:
                #                 Bio_Detail = "None" 
                #             try:
                #                 Instagram_Link = driver.find_elements(By.XPATH,"//div/a[@rel='nofollow ugc noreferrer noopener']")[0].text
                #             except:
                #                 Instagram_Link = "None"
                #             All_Records_Here = [Store_Average_Price,Product_Rating,Here_Next_Url,Seller_Name,Last_Active_Date,SoldItem,Rating,Followers,Bio_Detail,Instagram_Link]
                #             print(All_Records_Here,"_________________")
                #             with open('Store_Vintage_Product.csv', 'a', encoding='UTF8', newline='') as f:
                #                 writer = csv.writer(f)
                #                 writer.writerow(All_Records_Here)
                        
            except:
                pass

            time.sleep(10)
