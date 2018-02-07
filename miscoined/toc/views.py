from flask import render_template

from miscoined import app

from miscoined.toc.character import Character


@app.route("/toc")
@app.route("/toc/")
def character_create():
    return render_template(
        'toc/character.html',
        occupations=Character.OCCUPATIONS,
        investigative_categories=list(Character.CATEGORIES.keys()),
        character=Character.new(),
    )
