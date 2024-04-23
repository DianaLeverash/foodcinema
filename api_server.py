import requests
from random import randint
from constants import *


def get_info_about_dish(dish):
    params_info_about_dish = {"apiKey": API_KEY_FOOD, "query": dish}
    response = requests.get(BASE_URL_FOOD + GET_FOOD_INFO, params=params_info_about_dish)
    if len(response.json()["results"]) == 0:
        return "Error"
    return response.json()["results"][0]

def get_dish_calories(id):
    response = requests.get(BASE_URL_FOOD + GET_FOOD_CALORIES.replace("{{id}}", str(id)), params=PARAMS_FOOD_CALORIES)
    return int(response.json()["calories"])

def get_info_about_kino(calories):
    calories = int(calories)
    p = 1
    l = 100
    params_kino = {"page": p, "limit": l}
    if calories < 300:
        params_kino["genres.name"] = ["комедия", "боевик"]
    elif calories < 600:
        params_kino["genres.name"] = ["драма"]
    else:
        params_kino["genres.name"] = ["ужасы", "триллер"]
    response = requests.get(BASE_URL_KINO + GET_MOVE_INFO, headers={"X-API-KEY": API_KEY_KINO}, params=params_kino)
    return response.json()["docs"][randint(0, p * l - 1)]