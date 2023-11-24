import pytest

from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist
from games.adapters.repository import RepositoryException


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('DaveyJones', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('DaveyJones')

    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Alejandro', '51251255')
    repo.add_user(user)

    user2 = repo.get_user('Alejandro')
    assert user == user2


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('Hasbulla')
    assert user is None

def test_repository_can_retrieve_game_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_games = repo.get_number_of_games()

    # Check that the query returned 177 Articles.
    assert number_of_games == 877

def test_repository_can_add_and_retrieve_a_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game = Game(333333333, "Test Game")
    repo.add_game(game)

    retrieved_game = repo.get_game_by_id(game.game_id)
    assert retrieved_game == game

def test_repository_can_add_and_retrieve_a_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genre = Genre("Test Genre")
    repo.add_genre(genre)

    retrieved_genres = repo.get_genres()
    assert genre in retrieved_genres


def test_repository_can_add_and_retrieve_a_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User("TestUser", "password")
    game = Game(333333333, "Test Game")
    review = Review(user, game, 5, "Great game!")
    repo.add_user(user)
    repo.add_game(game)
    repo.add_review(review)

    retrieved_reviews = repo.get_reviews()
    assert review in retrieved_reviews

def test_repository_can_add_and_retrieve_a_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User("TestUser", "password")
    game = Game(333333333, "Test Game")
    review = Review(user, game, 5, "Great game!")
    repo.add_user(user)
    repo.add_game(game)
    repo.add_review(review)

    retrieved_reviews = repo.get_reviews()
    assert review in retrieved_reviews




def test_repository_can_add_and_retrieve_a_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    publisher = Publisher("New Publisher")
    repo.add_publisher(publisher)

    retrieved_publisher = repo.get_publisher("New Publisher")
    assert retrieved_publisher == publisher


def test_repository_can_toggle_favourite_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User("User1", "password")
    game = Game(555555, "New Game")
    repo.add_user(user)
    repo.add_game(game)

    # Toggle the game as a favorite
    result1 = repo.toggle_favourite(game, user)

    # Toggle it again, which should remove it from the favorites
    result2 = repo.toggle_favourite(game, user)

    liked_games = repo.get_liked_games(user)

    assert result1 is True
    assert result2 is False
    assert game.game_id not in liked_games



def test_repository_returns_average_rating(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User("User3", "password")
    game = Game(777777, "Game with Reviews")
    review1 = Review(user, game, 5, "Excellent game")
    review2 = Review(user, game, 3, "Average game")

    repo.add_user(user)
    repo.add_game(game)
    repo.add_review(review1)
    repo.add_review(review2)

    avg_rating = repo.get_average_rating(game.game_id)
    assert avg_rating == 4.0

def test_repository_returns_NA_for_average_rating_when_no_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game = Game(888888, "Game without Reviews")

    avg_rating = repo.get_average_rating(game.game_id)
    assert avg_rating == "N/A"


def test_repository_cannot_create_review_without_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game = Game(555555, "Game without Review User")
    repo.add_game(game)
    with pytest.raises(ValueError):
        review = Review(None, game, 4, "Good game")

def test_repository_cannot_create_review_for_non_existent_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    '''GAME IS NOT BEING ADDED TO REPO'''

    user = User("HappySingh", "HappisPassword")
    repo.add_user(user)

    # with pytest.raises(ValueError):
    with pytest.raises(ValueError):
        review = Review(user, None, 4, "Good game")



def test_repository_can_retrieve_all_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User("TestUser", "password")
    user2 = User("TestUser2", "password2")
    user3 = User("TestUser3", "password3")
    game = Game(333333333, "Test Game")
    review = Review(user, game, 5, "Great game!")
    review2 = Review(user2, game, 2, "Bad Game!")
    review3 = Review(user3, game, 3, "Its okay...")
    repo.add_user(user)
    repo.add_user(user2)
    repo.add_user(user3)
    repo.add_game(game)
    repo.add_review(review)
    repo.add_review(review2)
    repo.add_review(review3)

    retrieved_reviews = repo.get_reviews()

    assert str(retrieved_reviews) == "[Review(User: <User TestUser>, Game: <Game 333333333, Test Game>, Rating: 5, Comment: Great game!), Review(User: <User TestUser2>, Game: <Game 333333333, Test Game>, Rating: 2, Comment: Bad Game!), Review(User: <User TestUser3>, Game: <Game 333333333, Test Game>, Rating: 3, Comment: Its okay...)]"