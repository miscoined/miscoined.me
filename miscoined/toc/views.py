from flask import render_template, url_for, redirect, request, jsonify

from miscoined import app

import miscoined.toc.data as data
from miscoined.toc.character import Character


@app.route("/toc")
@app.route("/toc/")
def landing():
    return redirect(url_for('character'))


@app.route("/toc/character")
def character():
    return render_template("toc/character.html")


@app.route("/toc/api/character", methods=["GET", "POST"])
def character_create():

    if request.method == "POST":
        Character.put(request.get_json())
        return redirect(url_for('character_create'))

    return jsonify(Character.new())


@app.route("/toc/api/occupations")
def occupations():
    return jsonify(data.occupations())
