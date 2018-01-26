from wtforms import Form, StringField, validators

class CharacterCreateForm(Form):
  player = StringField('Player Name', [validators.DataRequired()])
  character = StringField('Character Name', [validators.DataRequired()])

