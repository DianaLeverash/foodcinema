from flask import Flask, request, render_template, redirect
from api_server import *

app = Flask(__name__)

data = [["борщец", "https://spoonacular.com/recipeImages/635684-312x231.jpg",
         "1+1", "https://image.openmoviedb.com/tmdb-images/w500/bGksau9GGu0uJ8DJQ8DYc9JW5LM.jpg"],

        ["борщец", "https://spoonacular.com/recipeImages/635684-312x231.jpg",
         "1+1", "https://image.openmoviedb.com/tmdb-images/w500/bGksau9GGu0uJ8DJQ8DYc9JW5LM.jpg"]
        ]
dishes = ["borsch", "fried potatoes", "dumplings", "cutlets", "Cannellini Bean and Asparagus Salad with Mushrooms"]

def creation_of_spisok(dish_hits):
    hits = []
    for dish in dish_hits:
        info_of_dish = get_info_about_dish(dish)
        id_of_dish = info_of_dish["id"]
        name_of_dish = info_of_dish["title"]
        image_of_dish = info_of_dish["image"]
        calories = get_dish_calories(id_of_dish)
        info_about_kino = get_info_about_kino(calories)
        name_of_film = info_about_kino["name"]
        film_description = info_about_kino["description"]
        year_of_release = info_about_kino["year"]
        image_of_film = info_about_kino["poster"]["previewUrl"]
        hits.append([name_of_dish, image_of_dish, name_of_film, image_of_film])
    return hits

@app.route('/')
def main():
    #return render_template('mainpage.html', data=data)
    return render_template('mainpage.html', data=creation_of_spisok(dishes))

spisok_of_eating_dishes = []
calories = 0
mas_of_history = []
with open("history.txt", "r") as f:
    mas_of_history = list(map(lambda x: x.rstrip(), f.readlines()))
@app.route('/create', methods=["POST", "GET"])
def main2():
    global calories, mas_of_history
    if request.method == "POST":
        if request.form["btn"] == "add":
            name_of_dish = request.form["dish"]
            if name_of_dish not in spisok_of_eating_dishes and name_of_dish != "":
                info_of_dish = get_info_about_dish(name_of_dish)
                if info_of_dish == "Error":
                    return render_template('food_choice_page.html', dishes=spisok_of_eating_dishes, mas_of_history=mas_of_history)
                name_of_dish = info_of_dish["title"]
                image_of_dish = info_of_dish["image"]
                calories += get_dish_calories(info_of_dish["id"])
                spisok_of_eating_dishes.append([name_of_dish, image_of_dish])
                with open("history.txt", "a") as file:
                    file.write(name_of_dish + "\n")
                with open("history.txt", "r") as f:
                    mas_of_history = list(map(lambda x: x.rstrip(), f.readlines()))
        if request.form["btn"] == "clear":
            f2 = open('history.txt', 'w')
            f2.close()
            mas_of_history = []
            return render_template('food_choice_page.html', dishes=spisok_of_eating_dishes,
                                   mas_of_history=mas_of_history)
        return redirect("/create")
    if request.method == "GET":
        return render_template('food_choice_page.html', dishes=spisok_of_eating_dishes, mas_of_history=mas_of_history)

name_of_film = ""
image_of_film = ""
film_description = ""
year_of_release = ""
genres = ""
@app.route('/film', methods=["POST", "GET"])
def main3():
    global name_of_film, image_of_film, film_description, year_of_release, genres
    if request.method == "POST":
        if request.form["btn"] == "add":
            name_of_dish = request.form["dish"]
            if name_of_dish not in spisok_of_eating_dishes:
                pass
        return redirect("/film")
    if request.method == "GET":
        if name_of_film == "":
            info_about_kino = get_info_about_kino(calories)
            name_of_film = info_about_kino["name"]
            film_description = info_about_kino["description"]
            year_of_release = info_about_kino["year"]
            film_genres = info_about_kino["genres"]
            for i in range(len(film_genres) - 1):
                genres += film_genres[i]["name"] + ", "
            genres += film_genres[-1]["name"]
            image_of_film = info_about_kino["poster"]["previewUrl"]
        return render_template('page_of_recommendation.html', data=spisok_of_eating_dishes,
                               film_text=name_of_film, film_image=image_of_film, film_description=film_description,
                               year_of_release=year_of_release, genres=genres)

if __name__ == '__main__':
    app.run()