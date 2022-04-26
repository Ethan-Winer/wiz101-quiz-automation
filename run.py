from selenium import webdriver
from time import sleep
from pygame import mixer
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, \
    ElementNotInteractableException
import os

from stuff import answer_map, link_map

driver = webdriver.Firefox(executable_path='D:\Programming\Geckodriver\geckodriver.exe',service_log_path=os.devnull)

def get_answer_list():
    answers = []
    for i in range(1, 5):
        answer = driver.find_element_by_css_selector('div.answer:nth-child(' + str(i) + ') > span:nth-child(2)').text
        answers.append(answer)
    return answers

def get_answer(question, topic):
    answers = get_answer_list()
    for i in range(0, len(answer_map[topic])):
        if answer_map[topic][i][0] == question:
            for k in range(0,4):
                if answer_map[topic][i][1] in answers[k]:
                    return k + 1

    print('guess')
    return 1

def safe_click(selector):
    clicked = False
    while not clicked:
        try:
            driver.find_element_by_css_selector(selector).click()
            clicked = True
        except NoSuchElementException or StaleElementReferenceException or ElementNotInteractableException:
            sleep(0.25)
            print('waiting to click safely')


mixer.init()
mixer.music.load('alert.mp3')
mixer.music.set_volume(0.4)

driver.get('https://www.wizard101.com/game')
sleep(1)
username = os.environ.get("wiz_101_username")
password = os.getenv("wiz_101_password")

driver.find_element_by_css_selector('#loginUserName').send_keys(username)
driver.find_element_by_css_selector('#loginPassword').send_keys(password)
sleep(0.25)
driver.find_element_by_css_selector('.wizardButtonInput > div:nth-child(2) > input:nth-child(1)').click()


# input('input after sign in')


for topic in link_map:
    driver.get(link_map[topic])
    sleep(5)
    for i in range(0, 12):
        print('current question: ' + str(i + 1))
        sleep(4)

        question = driver.find_element_by_css_selector('.quizQuestion').text
        answer_number = get_answer(question, topic)
        safe_click('div.answer:nth-child('+ str(answer_number) +') > span:nth-child(1) > a:nth-child(1)')
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

    onScoreScreen = False
    while not onScoreScreen:
        try:
            if driver.find_element_by_css_selector(".quizScore").text != '??':
                onScoreScreen = True
            else:
                sleep(0.25)
        except NoSuchElementException or ElementNotInteractableException:
            sleep(0.25)
    sleep(2)
sleep(3)
driver.close()