from flask import render_template, url_for, redirect, request, jsonify

from . import toc

from miscoined.toc.character import Character, occupations


@toc.route("/")
def landing():
    return redirect(url_for('toc.character_page'))


@toc.route("/character")
@toc.route("/character/<name>")
def character_page(name=None):
    return render_template("character.html", character_name=name)


@toc.route("/api/character", methods=["GET", "POST"])
@toc.route("/api/character/<name>", methods=["GET", "POST"])
def api_character(name=None):

    if request.method == "POST":
        return jsonify({'name': Character.put(request.get_json(), name=name)})
    character = Character.new() if name is None else Character.load(name)
    return jsonify(character)


@toc.route("/api/occupations")
def api_occupations():
    return jsonify(occupations())
