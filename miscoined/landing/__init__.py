from flask import Blueprint

landing = Blueprint("landing", __name__,
                    template_folder="templates",
                    static_folder="static",
                    static_url_path="/static/admin")
