from flask import render_template, url_for, redirect, request, jsonify

from miscoined import app

import miscoined.toc.data as data
from miscoined.toc.character import Character


@app.route("/toc")
@app.route("/toc/")
def landing():
    return redirect(url_for('character_create'))


@app.route("/toc/character", methods=["GET", "POST"])
def character_create():

    if request.method == "POST":
        Character.put(request.get_json())

    return render_template(
        'toc/character.html',
        character=Character.new(),
    )


@app.route("/toc/occupations")
def occupations():
    return jsonify(data.occupations())
