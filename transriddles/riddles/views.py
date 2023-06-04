from django.shortcuts import render
import requests
import random
import time

from .const import ASIAN_LANG, ARABIAN_LANG, OTHER_LANG, RIDDLES


def index(request):
    '''простая главная страница'''
    return render(request, 'riddles/index.html')


def riddles(request):
    '''страница с загадками'''

    def choice_riddle():
        """выбираем случайный фильм из списка"""
        a = random.choice(RIDDLES)
        return a

    def ru_to_asian():
        '''переводим с русского на случайный азаиатский'''
        random_lang = random.choice(ASIAN_LANG)
        CHAIN_LANG.append(random_lang)
        payload = {
            "q": CHOSEN_RIDDLE[0],
            "source": "ru",
            "target": random_lang[1]
        }
        response = requests.post(URL, json=payload, headers=headers)
        CHAIN_TRANSLATIONS.append(response.json()['data']['translations']['translatedText'])
        time.sleep(1)

    def asian_to_arabian():
        '''переводим с азиатского на случайный арабский'''
        random_lang = random.choice(ARABIAN_LANG)
        payload = {
            "q": CHAIN_TRANSLATIONS[-1],
            "source": CHAIN_LANG[-1][1],
            "target": random_lang[1]
        }
        CHAIN_LANG.append(random_lang)
        response = requests.post(URL, json=payload, headers=headers)
        CHAIN_TRANSLATIONS.append(response.json()['data']['translations']['translatedText'])
        time.sleep(1)

    def arabian_to_other():
        '''переводим с арабского на случайный другой'''
        random_lang = random.choice(OTHER_LANG)
        payload = {
            "q": CHAIN_TRANSLATIONS[-1],
            "source": CHAIN_LANG[-1][1],
            "target": random_lang[1]
        }
        CHAIN_LANG.append(random_lang)
        response = requests.post(URL, json=payload, headers=headers)
        CHAIN_TRANSLATIONS.append(response.json()['data']['translations']['translatedText'])
        time.sleep(1)

    def back_to_ru():
        '''переводим с другого обратно на русский'''
        payload = {
            "q": CHAIN_TRANSLATIONS[-1],
            "source": CHAIN_LANG[-1][1],
            "target": 'ru'
        }
        response = requests.post(URL, json=payload, headers=headers)
        CHAIN_TRANSLATIONS.append(response.json()['data']['translations']['translatedText'])
        time.sleep(1)

    # случайно выбранный фильм
    CHOSEN_RIDDLE = choice_riddle()
    # список языков перевода фильма
    CHAIN_LANG = []
    # список переводов названия фильма
    CHAIN_TRANSLATIONS = []

    URL = "https://deep-translate1.p.rapidapi.com/language/translate/v2"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "c061d433dfmsh04d2e5cd957fc9ep1833c9jsnc19d9c571a0e",
        "X-RapidAPI-Host": "deep-translate1.p.rapidapi.com"
        }

    ru_to_asian()
    asian_to_arabian()
    arabian_to_other()
    back_to_ru()
    context = {
        'chain_lang': CHAIN_LANG,
        'chain_translations': CHAIN_TRANSLATIONS,
        'riddle_after_translate': CHAIN_TRANSLATIONS[-1],
        'riddle_before_translate': CHOSEN_RIDDLE,
        }

    return render(request, 'riddles/riddles.html', context)
