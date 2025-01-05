from flask import Blueprint
from antipatterns.controllers import evaluate_antipattern

antipatterns_bp = Blueprint("antipatterns", __name__)

# Define las rutas
@antipatterns_bp.route("/evaluate", methods=["POST"])
def evaluate():
    return evaluate_antipattern()
