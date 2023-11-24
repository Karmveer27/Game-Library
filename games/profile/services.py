from games.adapters.repository import AbstractRepository
from games.authentication.services import UnknownUserException
from games.domainmodel.model import Game

def get_user(repo: AbstractRepository, username: str):
    user = repo.get_user(username)

    return user

def get_game(repo: AbstractRepository, gameID: int):
    game = repo.get_game_by_id(gameID)
    return game



def toggle_favourite(repo: AbstractRepository, game,user):
    gameAdded = repo.toggle_favourite(game,user)
    return gameAdded

def get_liked_games(repo: AbstractRepository,user):
    return repo.get_liked_games(user)

def get_liked_games_objects(repo: AbstractRepository,user):
    print("in services liked games obejctrs")
    print(repo.get_liked_games_objects(user))
    return repo.get_liked_games_objects(user)





