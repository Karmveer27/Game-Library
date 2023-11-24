from bisect import insort_left
from pathlib import Path
from typing import List
import os

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, User, Review, Publisher
from games.adapters.datareader.csvdatareader import GameFileCSVReader


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__games = list()
        self.__genres = list()
        self.__users = list()
        self.__reviews = list()
        self.__publisher = list()
        # self.__rating = list()
        self.__rating = {}


    def add_review(self, review: Review):
        super().add_review(review)
        self.__reviews.append(review)



    def get_reviews(self):
        return self.__reviews

    def get_reviews_for_game(self, game_id: int) -> List[Review]:
        game_reviews = []
        for review in self.__reviews:
            if review.game.game_id == game_id and review not in game_reviews:
                game_reviews.append(review)
        return game_reviews
    # def add_rating(self, rating):
    #     self.__rating.append(rating)
    #
    # def get_ratings(self):
    #     return self.__rating

    def add_rating(self, game_id, review):
        if game_id not in self.__rating:
            self.__rating[game_id] = []
        self.__rating[game_id].append(review.rating)

        # print("THIS IS THE RATING!!!!", self.__rating[game_id])

    # def get_ratings_for_game(self, game_id: int) -> List[int]:
    #     return self.__rating.get(game_id, [])

    # def get_ratings_for_game(self, game_id: int) -> List[int]:
    #     if game_id in self.__rating:
    #         return self.__rating[game_id]
    #     else:
    #         raise ValueError(f"Game ID {game_id} not found in ratings.")

    def get_ratings(self, game_id):
        # print("this is the entire dictionary ", self.__rating)
        if str(game_id) in self.__rating:
            print("get_ratings method gives this: ", self.__rating[str(game_id)])
            return self.__rating[str(game_id)]
        else:
            return []

    def get_average_rating(self, game_id):
        list_of_ratings = self.get_ratings(game_id)
        total_ratings = 0
        print("in get avewrage rating")
        print(list_of_ratings)
        if list_of_ratings is not None and len(list_of_ratings) > 0:
            for review in list_of_ratings:
                total_ratings += review

            return round((total_ratings / len(list_of_ratings)), 2)
        return "N/A"

    # def get_ratings(self, game_id):
    #     return self.__rating[game_id]

    # def get_ratings(self):
    #     all_ratings = []
    #     for ratings_list in self.__rating.values():
    #         all_ratings.extend(ratings_list)
    #     return all_ratings

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        print("In repo")
        print(user_name)
        print(self.__users)
        return next((user for user in self.__users if user.username.lower() == user_name.lower()), None)

    def add_game(self, game: Game):
        if isinstance(game, Game):
            insort_left(self.__games, game)

    def get_games(self) -> List[Game]:
        return self.__games

    def get_number_of_games(self):
        return len(self.__games)

    def get_game_by_id(self, id):
        for game in self.__games:
            if game.game_id == id:
                return game
        return None

    def add_genre(self, genre: Genre):
        if isinstance(genre, Genre):
            insort_left(self.__genres, genre)

    def get_genres(self) -> List[Genre]:
        return self.__genres

    def add_publisher(self, publisher: Publisher):
        if isinstance(publisher, Publisher):
            insort_left(self.__publisher, publisher)

    def toggle_favourite(self, game, user):
        print("getting in memory repo toggle fav")
        if game in user.favourite_games:
            #print("Game removed")
            user.remove_favourite_game(game)
            return False
        else:
            user.add_favourite_game(game)
            return True
            #print("Game added")

    def get_liked_games(self, user):
        liked_games_temp = user.favourite_games
        liked_games = [game.game_id for game in liked_games_temp]
        return liked_games

    def get_liked_games_objects(self, user):
        return user.favourite_games

def populate(data_path: Path, repo: AbstractRepository):
    directory_name = os.path.dirname(os.path.abspath(__file__))
    games_file_name = os.path.join(directory_name, "data/games.csv")
    reader = GameFileCSVReader(games_file_name)


    reader.read_csv_file()



    games = reader.dataset_of_games
    genres = reader.dataset_of_genres


    for game in games:
        repo.add_game(game)

    for genre in genres:
        repo.add_genre(genre)