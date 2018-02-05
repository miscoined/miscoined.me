from flask import render_template

from miscoined import app
from miscoined.toc.abilities import Abilities
from miscoined.toc.occupations import Occupations


@app.route("/toc")
@app.route("/toc/")
def character_create():
    return render_template(
        'toc/character.html',
        occupations=Occupations.OCCUPATIONS,
        investigative_categories=list(Abilities.CATEGORIES.keys()),
        investigative=Abilities.investigative,
        general=Abilities.general,
    )
