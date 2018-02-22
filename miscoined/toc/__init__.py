from flask import Blueprint

toc = Blueprint("toc", __name__,
                template_folder="templates",
                static_folder="static",
                url_prefix="/toc")
