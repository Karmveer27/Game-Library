import pytest

import os
from typing import List
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.library import services


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Hasbulla', 'PassHasbulla')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('Hasbulla') is user



def test_respository_can_retrieve_a_user(in_memory_repo):
    user_Guapo = User('Guapo', 'PassGuapo')
    in_memory_repo.add_user(user_Guapo)
    user = in_memory_repo.get_user('Guapo')
    assert user == User('Guapo', 'PassGuapo')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None

def test_repository_can_retrieve_game_count(in_memory_repo):
    number_of_games = in_memory_repo.get_number_of_games()

    # Check that the query returned 877 Games.
    assert number_of_games == 877

def test_repository_can_add_game(in_memory_repo):
    game = Game(
        79312356,
        'TesterGame'
    )
    in_memory_repo.add_game(game)
    assert in_memory_repo.get_game_by_id(79312356) is game

def test_repository_does_not_retrieve_a_non_existent_game(in_memory_repo):
    game = in_memory_repo.get_game_by_id(2)
    assert game is None

def test_repository_can_retrieve_initial_reviews(in_memory_repo):
    #Expected to receive 0 reviews as none are added initally.
    assert len(in_memory_repo.get_reviews()) == 0



def test_repository_can_add_and_retrieve_reviews_for_game(in_memory_repo):
    user1 = User('User1', 'Password1')
    user2 = User('User2', 'Password2')

    #Game used is Call of Duty, the Game_id for it is 7940.

    review1 = Review(user1, in_memory_repo.get_game_by_id(7940), 4, "Review 1")
    review2 = Review(user2, in_memory_repo.get_game_by_id(7940), 5, "Review 2")

    # in_memory_repo.add_game(game)

    user1.add_review(review1)
    in_memory_repo.get_game_by_id(7940).add_review(review1)

    user2.add_review(review2)
    in_memory_repo.get_game_by_id(7940).add_review(review2)

    in_memory_repo.add_review(review1)
    in_memory_repo.add_review(review2)

    game_reviews = in_memory_repo.get_reviews_for_game(7940)

    assert len(game_reviews) == 2
    assert review1 in game_reviews
    assert review2 in game_reviews


def test_repository_can_add_and_retrieve_ratings(in_memory_repo):


    retrevied_ratings = []

    user1 = User('User1', 'Password1')
    user2 = User('User2', 'Password2')

    #Game used is Call of Duty, the Game_id for it is 7940.

    review1 = Review(user1, in_memory_repo.get_game_by_id(7940), 4, "Review 1")
    review2 = Review(user2, in_memory_repo.get_game_by_id(7940), 5, "Review 2")

    #Adding review to the users reviews and adding the review to the memory repository

    user1.add_review(review1)
    in_memory_repo.get_game_by_id(7940).add_review(review1)

    user2.add_review(review2)
    in_memory_repo.get_game_by_id(7940).add_review(review2)

    in_memory_repo.add_review(review1)
    in_memory_repo.add_review(review2)

    #retreieving reviews for the Call of Duty Game.

    game_reviews = in_memory_repo.get_reviews_for_game(7940)

    for review in in_memory_repo.get_reviews():
        retrevied_ratings.append(review.rating)

    #Ensuring the ratings of 5 and 4 are in the reviews.

    assert 5 in retrevied_ratings
    assert 4 in retrevied_ratings


def test_repository_returns_empty_list_for_nonexistent_ratings(in_memory_repo):
    game_id = 2
    retrieved_ratings = in_memory_repo.get_ratings(game_id)
    assert retrieved_ratings == []




def test_repository_can_add_and_retrieve_genres(in_memory_repo):

    #Creating Genres to add
    genre1 = Genre('Action')
    genre2 = Genre('Adventure')

    #Adding Genres to the repository
    in_memory_repo.add_genre(genre1)
    in_memory_repo.add_genre(genre2)

    genres = in_memory_repo.get_genres()

    #If the number of genres is 26, the two new genres have been added.
    assert len(genres) == 26

    #Testing to see if genres are added.
    assert genre1 in genres
    assert genre2 in genres

def test_repository_can_retrieve_games_by_genre(in_memory_repo):

    #Creating Genre
    genre = Genre('Action')

    #Creating Games
    game1 = Game(1, 'Game1')
    game2 = Game(2, 'Game2')
    game3 = Game(3, 'Game3')

    #Adding genre and games to the repository

    in_memory_repo.add_genre(genre)
    in_memory_repo.add_game(game1)
    in_memory_repo.add_game(game2)
    in_memory_repo.add_game(game3)

    #Linking the games to their associated genre. Only linking game1 and game2 to the Genre.

    game1.genres.append(genre)
    game2.genres.append(genre)

    #Retreieving games of the genre Action.

    games = services.games_of_specific_genre(in_memory_repo, 'Action')

    assert len(games) == 382

    #Expecting game 3 to not be in the games list since it is not linked to the genre 'Action.'
    assert game2 in games
    assert game3 not in games

