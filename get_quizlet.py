import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By

import time
import json


def main():

    IDs = []

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    browser = webdriver.Chrome("C:\\Users\\green\\Desktop\\Python code\\chromedriver_win32\\chromedriver.exe", options=options)

    for ID in IDs:
        browser.get(f"https://quizlet.com/gb/{ID}")

        time.sleep(2)

        data = []
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for terms in soup.find_all("div", {"class": "SetPageTerms-term"}):
            tup = terms.find_all("span", {"class": "TermText"})
            data.append([tup[0].getText(), tup[1].getText()])

        try:
            title = browser.find_element(By.XPATH, "/html/body/div[4]/div[3]/div[1]/div[2]/div/div[1]/div[1]/div/div/div[1]/div[1]/h1").text
        except Exception as e:
            title = browser.find_element(By.XPATH, "/html/body/div[5]/div[3]/div[1]/div[2]/div/div[1]/div[1]/div/div/div[1]/div[1]/h1").text
        
        with open("quizzes.json", "r") as f:
            jsondata = json.load(f)
            jsondata[title] = data
        
        with open("quizzes.json", "w") as f:
            json.dump(jsondata, f, indent=4)
    
    browser.close()


if __name__ == "__main__":
    main()