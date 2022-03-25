from selenium import webdriver
from time import sleep
from pygame import mixer
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from stuff import answer_map, list_of_links

driver = webdriver.Firefox(executable_path='D:\Programming\Geckodriver\geckodriver.exe')

def get_answer_list():
    answers = []
    for i in range(1, 5):
        answer = driver.find_element_by_css_selector('div.answer:nth-child(' + str(i) + ') > span:nth-child(2)').text
        answers.append(answer)
    return answers

def get_answer(question):
    answers = get_answer_list()
    if question in answer_map:
        for i in range(0, 4):
            if answers[i] in answer_map[question] or answer_map[question] in answers[i]:
                return str(i+1)

    mixer.music.play()
    print('1 -- 2\n3 -- 4')
    number = input('question not found bruh. give number: ')
    print("'" + question + "'" + ': ' + "'" +driver.find_element_by_css_selector('div.answer:nth-child(' + number + ') > span:nth-child(2)').text + "',")
    return number

def safe_click(selector):
    clicked = False
    while not clicked:
        try:
            driver.find_element_by_css_selector(selector).click()
            clicked = True
        except Exception:
            sleep(0.25)
            print('waiting to click safely')


mixer.init()
mixer.music.load('alert.mp3')
mixer.music.set_volume(0.4)

driver.get('https://www.wizard101.com/game')

input('input after sign in')


for link in list_of_links:
    driver.get(link)
    sleep(5)
    for i in range(0, 12):
        print('current question: ' + str(i + 1))
        sleep(4)

        question = driver.find_element_by_css_selector('.quizQuestion').text
        answer_number = get_answer(question)
        safe_click('div.answer:nth-child('+ answer_number +') > span:nth-child(1) > a:nth-child(1)')
        sleep(1)

        safe_click('#nextQuestion')
        if i < 11:
            loaded = False
            while not loaded:
                try:
                    if question != driver.find_element_by_css_selector('.quizQuestion').text:
                        loaded = True
                except NoSuchElementException:
                    sleep(0.25)
                except StaleElementReferenceException:
                    sleep(0.25)
    mixer.music.play()
    input("move to next confirm 1")
    input("move to next confirm 2")
input('input to close driver')
driver.close()