from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import csv
import time
from selenium.webdriver.common.action_chains import ActionChains

def main(SchoolName):
    CommetsArr = []
    AuthorsArr = []
    try:
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--lang=en-GB")
        driver = webdriver.Chrome(options=options)

        driver.get('https://maps.google.com')
        search_query = SchoolName
        search_box = driver.find_element(By.ID, "searchboxinput")
        search_box.send_keys(search_query + Keys.ENTER)

        driver.implicitly_wait(5)

        try:
            first_div = driver.find_element(By.CSS_SELECTOR, 'div.Nv2PK.tH5CWc.THOPZb:first-of-type')
            first_link = first_div.find_element(By.CLASS_NAME, "hfpxzc")
            first_link.click()
        except:
            print("Page found")

        time.sleep(5)

        reviews = driver.find_elements(By.CSS_SELECTOR, 'div.MyEned ')
        authors = driver.find_elements(By.CSS_SELECTOR, 'div.d4r55 ')

        for review, author in zip(reviews, authors):
            comments = review.find_elements(By.CSS_SELECTOR, 'span.wiI7pd')
            Author = author.text.strip()
            for comment in comments:
                Comment = comment.text
                CommetsArr.append(Comment)
                AuthorsArr.append(Author)

    except Exception as e:
        print("An error occurred:", str(e))


    return CommetsArr, AuthorsArr




