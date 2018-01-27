from flask import render_template

from miscoined import app

@app.route("/")
def main():
  return render_template('landing.html')

@app.route("/cv")
def cv_html():
  return render_template("cv.html")
