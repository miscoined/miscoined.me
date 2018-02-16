from flask import render_template, url_for, redirect, request, jsonify

from miscoined import app

import miscoined.toc.data as data
from miscoined.toc.character import Character


@app.route("/toc")
@app.route("/toc/")
def landing():
    return redirect(url_for('character'))


@app.route("/toc/character")
def character_page():
    return render_template("toc/character.html")


@app.route("/toc/api/character")
@app.route("/toc/api/character/<name>", methods=["GET", "POST"])
def api_character(name=None):

    if request.method == "POST":
        Character.put(request.get_json(), name=name)
        return redirect(url_for('character_page', name=name))
    character = Character.new() if name is None else Character.load(name)
    return jsonify(character)


@app.route("/toc/api/occupations")
def occupations():
    return jsonify(data.occupations())
