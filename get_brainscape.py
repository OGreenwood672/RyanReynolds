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

    IDs = ["11-inside-the-atom-7172891/packs/11646512", "12-stable-and-unstable-nuclei-7324271/packs/11646512", "13-photons-7324382/packs/11646512", "14-particles-and-antiparticles-7324491/packs/11646512",
            "15-particle-interactions-7324793/packs/11646512", "21-the-particle-zoo-7337192/packs/11646512", "22-particle-sorting-7337232/packs/11646512", "23-leptons-at-work-7337288/packs/11646512",
            "24-quarks-and-antiquarks-7337367/packs/11646512", "25-conservation-rules-7337521/packs/11646512"]
    titles = ["inside-atom", "stable and unstable", "photons", "particles and antiparticles", "particle interaction", "particle zoo", "particle sorting", "leptons", "quarks and antiquarks", "conservation"]

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    browser = webdriver.Chrome("C:\\Users\\green\\Desktop\\Python code\\chromedriver_win32\\chromedriver.exe", options=options)

    for title, ID in zip(titles, IDs):
        browser.get(f"https://www.brainscape.com/flashcards/{ID}")

        time.sleep(2)

        data = []
        soup = BeautifulSoup(browser.page_source, "html.parser")
        questions = soup.find_all(class_="card-question")
        answers = soup.find_all(class_="card-answer")

        questions = list(map(lambda x: [p.text for p in x.find_all("h2")], questions))
        answers = list(map(lambda x: [p.text for p in x.find_all("h3")], answers))

        
        print("Got data")
        
        with open("quizzes.json", "r") as f:
            jsondata = json.load(f)
        
        jsondata[title] = [list(x) for x in zip(questions, answers)]
        
        with open("quizzes.json", "w") as f:
            json.dump(jsondata, f, indent=4)
        
        print("Saved")
    
    browser.close()


if __name__ == "__main__":
    main()