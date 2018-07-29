from flask import render_template

from . import landing


@landing.route("/")
def main():
    return render_template('landing.html')


@landing.route("/cv")
def cv():
    return render_template("cv.html")
