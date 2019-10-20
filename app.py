from flask import Flask
from flask import render_template
from flask import request
import requests, json
app = Flask(__name__)


def construct_json(ingredient):
    ing_drinks = []
    req = requests.get("https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=%s" % ingredient)
    if not req.text:
        return 0
    jdrinks = json.loads(req.text)
    if jdrinks['drinks'] is None:
        return 0
    for drink in jdrinks['drinks']:
        ing_drinks.append(drink['strDrink'])
    return set(ing_drinks)


@app.route("/", methods=['GET'])
def ingredients():
    return render_template("ingredients.html")

@app.route("/result", methods=['POST'])
def results(ingredient1=None):
    ingredient1 = request.form['ingredient1']
    ingredient2 = request.form['ingredient2']
    ingredient3 = request.form['ingredient3']
    ing1_drinks = construct_json(ingredient1)
    ing2_drinks = construct_json(ingredient2)
    ing3_drinks = construct_json(ingredient3)

    if ing1_drinks is not 0 and ing2_drinks is not 0 and ing3_drinks is not 0:
        combine = ing1_drinks & ing2_drinks & ing3_drinks

    if combine:
        return render_template("existing.html", ing1_drinks=ing1_drinks, ing2_drinks=ing2_drinks, ing3_drinks=ing3_drinks)
    else:
        return render_template("new.html", ing1_drinks=ing1_drinks, ing2_drinks=ing2_drinks, ing3_drinks=ing3_drinks)