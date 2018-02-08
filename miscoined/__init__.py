from flask import Flask

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

import miscoined.landing.views  # noqa: E402
import miscoined.toc.views      # noqa: E402,F401
