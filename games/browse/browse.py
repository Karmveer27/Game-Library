from flask import Blueprint

from games.browse import services
from games.adapters.repository import AbstractRepository

browse_blueprint = Blueprint ("games_bp", __name__)

@browse_blueprint.route("/browse", methods=["GET"])
def browse_games():
    number_of_games = services.get_games(repo.repo_instance)
    all_games = services.get_games(repo.repo_instance)
    return render_template(
        'browse.html',

    )