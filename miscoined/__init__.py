from flask import Flask

from config import Config
from .landing import landing
from .toc import toc

app = Flask(__name__)
app.config.from_object(Config)

import miscoined.landing.views  # noqa: E402,F401
import miscoined.toc.views      # noqa: E402,F401

app.register_blueprint(landing)
app.register_blueprint(toc, url_prefix="/toc")
