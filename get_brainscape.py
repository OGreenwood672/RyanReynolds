# card-answer & card-question
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By

import time
import json
import fuckit


def main():

    titles = []
    IDs = []

    with open("urls.txt") as f:
        for line in f.readlines():
            string = line.split("=")
            titles.append(string[0])
            IDs.append(string[1])

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    browser = webdriver.Chrome("C:\\Users\\green\\Desktop\\Python code\\chromedriver_win32\\chromedriver.exe", options=options)

    for title, ID in zip(titles, IDs):
        browser.get(f"https://www.brainscape.com/flashcards/{ID}")

        time.sleep(2)

        data = []
        soup = BeautifulSoup(browser.page_source, "html.parser")
        questions_src = soup.find_all(class_="card-question")
        answers_src = soup.find_all(class_="card-answer")

        questions = []
        answers = []

        for question in questions_src:
            res = []
            for p in [*question.find_all("p")]:#, *question.find_all("h3"), *question.find_all("h2")]:
                res.append(p.text)
            for img in question.find_all("img"):
                res.append("\n" + img["data-src"])
            questions.append(res)
        
        
        for answer in answers_src:
            res = []
            for p in [*answer.find_all("p")]:#, *answer.find_all("h3"), *answer.find_all("h2")]:
                res.append(p.text)
            for img in answer.find_all("img"):
                res.append("\n" + img["data-src"])
            answers.append(res)
        
        print("Got data")
        
        with open("quizzes.json") as f:
            jsondata = json.load(f)
        
        jsondata[title] = [list(x) for x in zip(questions, answers)]
        
        with open("quizzes.json", "w") as f:
            json.dump(jsondata, f, indent=4)
        
        print("Saved")
    
    browser.close()


if __name__ == "__main__":
    main()