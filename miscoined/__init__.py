from flask import Flask
app = Flask(__name__)

import miscoined.cv.views
import miscoined.toc.views