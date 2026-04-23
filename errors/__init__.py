# errors/__init__.py

from flask import Blueprint

errors_bp = Blueprint("errors_bp", __name__,template_folder="templates"   )

from errors import handlers