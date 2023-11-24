from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game


def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()

def get_games(repo: AbstractRepository):
    games = repo.get_games()
    games_dicts = []
    for game in games:
        game_dict = {
            'game_id': game.game_id,
            'title': game.title,
            'release_date': game.release_date,
            'price': game.price,
            'description': game.description,
            'image_url': game.image_url,
            'genre' : game.genres,
            'publisher' : game.publisher.publisher_name
            # 'genre': [genre.genre_name for genre in game.genres]
        }
        games_dicts.append(game_dict)
    return games_dicts
def get_game_by_id(id : int, repo : AbstractRepository):
    game = repo.get_game_by_id(id)
    return game

def get_genres(repo : AbstractRepository):
    genres = repo.get_genres()
    genre_name_list = []

    for genre in genres:
        genre_name_list.append(genre.genre_name)


    return genre_name_list

def is_game_of_genre(game, required_genre):
    list_of_genre_names = [genre.genre_name for genre in game.genres]

    if required_genre in list_of_genre_names:
        return True
    return False

# def is_game_of_genre(game: Game, required_genre):
#     list_of_given_genres = game.genres
#
#
#     list_of_genre_names = []
#
#     for genre in list_of_given_genres:
#         list_of_genre_names.append(genre.genre_name)
#
#     if required_genre in list_of_genre_names:
#         return True
#     return False





def games_of_specific_genre(repo: AbstractRepository, required_genre):
    games = repo.get_games()
    games_genre_based = []

    for individual_game in games:
        if is_game_of_genre(individual_game, required_genre):
            games_genre_based.append(individual_game)

    return games_genre_based