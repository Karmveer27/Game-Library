import abc
from typing import List

from games.domainmodel.model import Game, Genre, User, Review, Publisher

repository_instance = None

class RepositoryException(Exception):
    def __init__(self, message = None):
        print (f'RepositoryException: {message}')

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User named user_name from the repository.

        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError


    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError



    @abc.abstractmethod
    def add_review(self, review: Review):

        if review.user is None or review not in review.user.reviews:
            raise RepositoryException("Review not correctly attached to a User")
        if review.comment is None or review not in review.game.reviews:
            raise RepositoryException("Review not correctly attached to a Game")

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the reviews attached in the repository. """
        raise NotImplementedError


    @abc.abstractmethod
    def get_games(self) -> List[Game]:
        """returns a list of games"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_games(self):
        """returns number of games in the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_game(self, game: Game):
        """adds game to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_game_by_id(self,id):
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """adds genre to the repository"""
        raise NotImplementedError

    def get_genre_by_name(self, genre_name: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        """returns unique genres"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_rating(self, game_id, rating):
        """Adds the rating to rating"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_ratings(self, game_id):
        "returns ratings"
        raise NotImplementedError

    @abc.abstractmethod
    def add_publisher(self, publisher: Publisher):
        """adds genre to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def toggle_favourite(self, game, user):
        raise NotImplementedError

    @abc.abstractmethod
    def get_liked_games(self, user):
        raise NotImplementedError

    @abc.abstractmethod
    def get_liked_games_objects(self, user):
        raise NotImplementedError

    @abc.abstractmethod
    def get_average_rating(self, game_id):
        raise NotImplementedError




