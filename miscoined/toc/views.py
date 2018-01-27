from flask import render_template, request, flash

from miscoined import app
from miscoined.toc.forms import CharacterCreateForm

@app.route("/toc")
@app.route("/toc/")
def character_create():
  form = CharacterCreateForm(request.form)
  if form.validate():
    flash('Made character {} for player {}'.format(form.player.data,
			    form.character.data))
    return redirect(url_for('character_create'))
  return render_template('toc/toc.html', form=form)
