import requests
from selenium import webdriver
from time import sleep

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


def find_answer_box(question, answers):
    response = requests.get('https://finalbastion.com/Trivia_Machine/livesearch.php?q=' + question).text
    if len(response) < 1000:
        for i in range(0, 4):
            if answers[i] in response:
                return 'div.answer:nth-child('+str(i + 1) +') > span:nth-child(1) > a:nth-child(1)'
    return 'div.answer:nth-child(1) > span:nth-child(1) > a:nth-child(1)'

def get_answer_list(driver):
    answers = []
    for i in range(1, 5):
        answer = driver.find_element_by_css_selector('div.answer:nth-child(' + str(i) + ') > span:nth-child(2)').text
        answers.append(answer)
    return answers

def safe_click(selector, driver):
    clicked = False
    while not clicked:
        try:
            driver.find_element_by_css_selector(selector).click()
            clicked = True
        except Exception:
            sleep(0.25)
            print('bruh')

driver = webdriver.Firefox(executable_path="D:\Programming\Geckodriver\geckodriver.exe")

list_of_links = [
    'https://www.wizard101.com/quiz/trivia/game/famous-poets',
    'https://www.wizard101.com/quiz/trivia/game/weather-trivia',
    'https://www.wizard101.com/quiz/trivia/game/dinosaur-trivia',
    'https://www.wizard101.com/quiz/trivia/game/wizard101-marleybone-trivia',
    'https://www.wizard101.com/quiz/trivia/game/american-presidents-trivia',
    'https://www.wizard101.com/quiz/trivia/game/book-quotes-trivia',
    'https://www.wizard101.com/quiz/trivia/game/english-punctuation-trivia',
    'https://www.wizard101.com/quiz/trivia/game/greek-mythology-trivia',
    'https://www.wizard101.com/quiz/trivia/game/norse-mythology-trivia',
    'https://www.wizard101.com/quiz/trivia/game/state-capitals-trivia'

]

driver.get('https://www.wizard101.com/game')

input('input after sign in')

for link in list_of_links:
    driver.get(link)
    sleep(5)
    for i in range(0, 12):
        answers = get_answer_list(driver)
        question = driver.find_element_by_css_selector('.quizQuestion').text

        box = find_answer_box(question, answers)

        safe_click(box, driver)
        sleep(1)

        safe_click('#nextQuestion', driver)

        loaded = False
        while not loaded:
            try:
                if question != driver.find_element_by_css_selector('.quizQuestion').text:
                    loaded = True
            except NoSuchElementException:
                sleep(0.25)
            except StaleElementReferenceException:
                sleep(0.25)
        sleep(4)
    input("move to next confirm 1")
    input("move to next confirm 2")
input('input to close driver')
driver.close()