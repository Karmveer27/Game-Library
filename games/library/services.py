

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, make_review
import games.adapters.repository as repo


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

class NonExistentGameException(Exception):
    pass

class UnknownUserException(Exception):
    pass

def add_review(game_id: int, review_text: str, review_rating: int, user_name: str, repo: AbstractRepository):

    # print(f"Adding review to game with ID: {game_id}")
    # print(f"The name of the user is {user_name}")


    game = repo.get_game_by_id(int(game_id))
    if game is None:
        raise NonExistentGameException



    user = repo.get_user(user_name)
    # print("USER NAME ISSSSS!!!!!!: ", user.username)


    if user is None:
        raise UnknownUserException

    review = make_review(user, game, review_rating, review_text)

    repo.add_review(review)
    #repo.add_rating(review.rating)
    repo.add_rating(game_id, review)

def get_average_rating(game_id: int, repo: AbstractRepository):
    average_rating = repo.get_average_rating(game_id)
    return average_rating
    # list_of_ratings = repo.get_ratings(game_id)
    # total_ratings = 0
    # print("in get avewrage rating")
    # print(list_of_ratings)
    # if list_of_ratings is not None and len(list_of_ratings) > 0:
    #     for review in list_of_ratings:
    #         total_ratings += review.rating
    #
    #     return round((total_ratings / len(list_of_ratings)), 2)
    # return "N/A"









def get_user(repo: AbstractRepository, username: str):
    user = repo.get_user(username)

    return user
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


def get_liked_games(repo: AbstractRepository,user):
    return repo.get_liked_games(user)
