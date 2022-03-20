import requests
from selenium import webdriver
from time import sleep

def find_answer_box(question, answers):
    response = requests.get('https://finalbastion.com/Trivia_Machine/livesearch.php?q=' + question).text
    if len(response) < 1000:
        for i in range(0, 4):
            if answers[i] in response:
                return i
    return 1

def get_answer_list(driver):
    answers = []
    for i in range(0, 4):
        answer = driver.find_element_by_css_selector('div.answer:nth-child(' + str(i) + ') > span:nth-child(2)').text
        answers.append(answer)
    return answers

driver = webdriver.Firefox(executable_path="D:\Programming\Geckodriver\geckodriver.exe")

list_of_links = [
    'https://www.wizard101.com/quiz/trivia/game/famous-poets',
    'https://www.wizard101.com/quiz/trivia/game/weather-trivia',
    'https://www.wizard101.com/quiz/trivia/game/dinosaur-trivia',
    'https://www.wizard101.com/quiz/trivia/game/wizard101-marleybone-trivia'
]

for link in list_of_links:
    driver.get(link)
