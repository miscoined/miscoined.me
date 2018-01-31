from flask import render_template, request, redirect, url_for

from miscoined import app
from miscoined.toc.abilities import Abilities


@app.route("/toc")
@app.route("/toc/")
def character_create():
    return render_template(
        'toc/toc.html',
        investigative_abilities=Abilities.investigative(),
        general_abilities=Abilities.general()
    )
