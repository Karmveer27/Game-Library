import pytest

from sqlalchemy.exc import IntegrityError

from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist
from games.adapters.database_repository import SqlAlchemyRepository

def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                          {'username': new_name, 'password': new_password})
    row = empty_session.execute('SELECT user_id from users where username = :username',
                                {'username': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT user_id from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_genre(empty_session):
    empty_session.execute('INSERT INTO genres (genre_name) VALUES (:genre_name)',
                          {'genre_name': 'TESTER GENRE'})

    row = empty_session.execute('SELECT genre_name from genres').fetchone()
    return row[0]



def make_genre():
    genre = Genre("TESTER GENRE")
    return genre


def make_user():
    user = User("Andrew", "Andrew123")
    return user

def make_game():
    game = Game(7777777, "Tester Game")
    return game


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "Andrew123"))
    users.append(("Cindy", "Cindy1234"))
    insert_users(empty_session, users)

    expected = [
        User("Andrew", "Andrew123"),
        User("Cindy", "Cindy1234")
    ]

    print('database getting::: ', empty_session.query(User).all())
    print('expected        ::: ', expected)

    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("Andrew", "Andrew123")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("Andrew", "Andrew123"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Andrew", "AndrewSecondUser")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_genres(empty_session):
    name_of_inserted_genre = insert_genre(empty_session)
    expected_genre = make_genre()
    fetched_genre = empty_session.query(Genre).one()

    assert expected_genre == fetched_genre
    assert name_of_inserted_genre == fetched_genre.genre_name

##bnew
def test_user_mapping(empty_session):
    def test_user_mapping(empty_session):
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': 'TestUser', 'password': 'Password1'})

        row = empty_session.execute('SELECT user_id from users where username = :username',
                                    {'username': 'TestUser'}).fetchone()

        assert row == (1)


def test_publisher_mapping(empty_session):
    publisher_name = "Test Publisher"


    try:
        empty_session.execute('INSERT INTO publishers (name) VALUES (:name)',
                              {'name': publisher_name})

        # inserted_publisher = empty_session.query(Publisher).filter_by(publisher_name=publisher_name).one()
        publisher = empty_session.execute('SELECT name from publishers where name = :name',
                                    {'name': publisher_name}).fetchone()

        assert publisher[0] == publisher_name

    except Exception as e:
        print(f"Error: {e}")
        assert False, f"An error occurred: {e}"


def test_review_mapping(empty_session):


    user = User("TestUser", "Password23")
    game = Game(11111111, "Test Game")
    review_text = "Great game! Great Developers!!!"
    rating = 5

    try:

        # Insert the review into the database using raw SQL query
        empty_session.execute('INSERT INTO reviews (review_id, review_text, rating, game_id, user_id) '
                              'VALUES (:review_id, :review_text, :rating, :game_id, :user_id)',
                              {'review_id': 22, 'review_text': review_text,
                               'rating': rating, 'game_id': game.game_id, 'user_id': 1})

        # Retrieve the inserted review from the database
        retrieved_review = empty_session.execute('SELECT review_text, rating FROM reviews '
                                                 'WHERE game_id = :game_id AND review_text = :review_text',
                                                 {'game_id': game.game_id, 'review_text': review_text}).fetchone()

        # Assert that the retrieved review matches the inserted values
        assert retrieved_review[0] == review_text
        assert retrieved_review[1] == rating

    except Exception as e:
        print(f"Error: {e}")
        assert False, f"An error occurred: {e}"
