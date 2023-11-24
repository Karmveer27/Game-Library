import sqlite3
from abc import ABC
from typing import List


import sqlalchemy.exc
from sqlalchemy.orm import scoped_session,aliased
from sqlalchemy.exc import NoResultFound




from games.adapters.repository import AbstractRepository, RepositoryException
from games.domainmodel.model import Review, User, Genre, Game, Publisher, Wishlist


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()

class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__username == username).one()
        except NoResultFound:

            pass

        return user


    def add_user(self, user: User):
        """ Adds a User to the repository. """
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def add_review(self, review: Review):
        print("adding review1")
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()



    def get_reviews(self):
        with self._session_cm as scm:
            return scm.session.query(Review).all()

    def get_games(self) -> List[Game]:
        with self._session_cm as scm:
            return scm.session.query(Game).all()


    def get_number_of_games(self):
        with self._session_cm as scm:
            return scm.session.query(Game).count()

    def add_game(self, game: Game):
        #print("add game")
        with self._session_cm as scm:
            scm.session.merge(game)
            scm.commit()

    def get_game_by_id(self, id):
        try:
            with self._session_cm as scm:
                game = self._session_cm.session.query(Game).filter(Game._Game__game_id == id).first()
                #print(game)
                return game
        except NoResultFound:
            return None

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()

    def get_genres(self) -> List[Genre]:
        with self._session_cm as scm:
            return scm.session.query(Genre).all()

    def add_rating(self, game_id, review):
        print("adding review2")
        with self._session_cm as scm:
            scm.session.add(review)
            scm.session.commit()

    def get_ratings(self, game_id):
        with self._session_cm as scm:
            print("getting to rating")
            reviews = scm.session.query(Review).all()

            return reviews

    def get_average_rating(self, game_id):
        list_of_ratings = self.get_ratings(game_id)
        total_ratings = 0
        print("in get avewrage rating")
        print(list_of_ratings)
        if list_of_ratings is not None and len(list_of_ratings) > 0:
            for review in list_of_ratings:
                total_ratings += review.rating

            return round((total_ratings / len(list_of_ratings)), 2)
        return "N/A"



    def toggle_favourite(self, game, user):
        game_id = game.game_id

        with self._session_cm as scm:
            user = scm.session.query(User).filter(User._User__username == user.username).first()
            user_id = user._User__user_id
            #print(user_id)
            wishlist = scm.session.query(Wishlist).filter(Wishlist._Wishlist_username == user.username).first()
            if wishlist is None:
                # If the wishlist doesn't exist, create a new one.
                wishlist = Wishlist(user)
                wishlist._Wishlist_username = wishlist.get_username()
                wishlist._Wishlist_user = user_id
                scm.session.add(wishlist)



            if game_id in [item._Game__game_id for item in wishlist._Wishlist__list_of_games]:
                print("Entering if item")

                wishlist._Wishlist__list_of_games = [item for item in wishlist._Wishlist__list_of_games if item._Game__game_id != game_id]
                scm.commit()
                return False
            else:
                print("Entering else item")

                game = scm.session.query(Game).filter(Game._Game__game_id==game_id).first()
                if game:
                    wishlist._Wishlist__list_of_games.append(game)
                    scm.commit()
                    return True
                else:

                    return False

    def get_liked_games(self, user):
        with self._session_cm as scm:
            wishlist = scm.session.query(Wishlist).filter(Wishlist._Wishlist_user == user._User__user_id).first()

            if wishlist:
                liked_games = [game.game_id for game in wishlist._Wishlist__list_of_games]
                return liked_games
            else:
                return []

    def get_liked_games_objects(self, user):
        with self._session_cm as scm:
            wishlist = scm.session.query(Wishlist).filter(Wishlist._Wishlist_user == user._User__user_id).first()

            if wishlist:
                liked_games = wishlist._Wishlist__list_of_games
                return liked_games
            else:
                return []





    def add_publisher(self, publisher: Publisher):
        with self._session_cm as scm:
            scm.session.merge(publisher)
            scm.commit()

    def get_publisher(self, publisherName):

        with self._session_cm as scm:
            publisher = scm.session.query(Publisher).filter(Publisher._Publisher__publisher_name == publisherName).first()

        if publisher:
            return publisher

        else:
            return "No publisher found."
