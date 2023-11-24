from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game


def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()

def get_games(repo: AbstractRepository):
    games = repo.get_games()
    games_dicts = []
    for game in games:
        games_dicts = {
            'game_id': game.game_id,
            'title': game.title,
            'game_url': game.release_date

        }
        games_dicts.append(games_dicts)
    return games_dicts