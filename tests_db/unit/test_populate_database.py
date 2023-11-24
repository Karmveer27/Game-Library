from sqlalchemy import select, inspect

from games.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['game_genres', 'game_wishlist', 'games', 'genres', 'publishers', 'reviews', 'users', 'wishlist']

def test_database_populate_select_all_games(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_games_table = inspector.get_table_names()[2]

    print(name_of_games_table)

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_games_table]])
        result = connection.execute(select_statement)

        all_game_names = []
        for row in result:
            all_game_names.append(row['game_title'])

        test_list = []

        for i in range(5):
            test_list.append(all_game_names[i])

        assert test_list == ['Xpand Rally', 'Call of Duty® 4: Modern Warfare®', 'Nikopol: Secrets of the Immortals', 'Max Payne', 'BC Kings']

def test_database_populate_select_all_users(database_engine):

    database_engine.connect().execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                          {'username': 'TesterTerminator', 'password': 'RandomPasswordTerminator2'})

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[6]
    print("nameeee: ", name_of_users_table)

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['username'])

        assert all_users == ['TesterTerminator']

        #'1,TesterTerminator,RandomPasswordTerminator'


def test_database_populate_select_all_reviews(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[5]

    review_text = "Great game! Great Developers!!!"
    rating = 5

    # Insert the review into the database using raw SQL query
    database_engine.connect().execute('INSERT INTO reviews (review_id, review_text, rating, game_id, user_id) '
                          'VALUES (:review_id, :review_text, :rating, :game_id, :user_id)',
                          {'review_id': 22, 'review_text': review_text,
                           'rating': rating, 'game_id': 8888881, 'user_id': 5})


    with database_engine.connect() as connection:
        # query for records in table reviews
        select_statement = select([metadata.tables[name_of_reviews_table]])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:
            all_reviews.append((row['review_id'], row['user_id'], row['game_id'], row['review_text']))

        assert all_reviews == [(22, 5, 8888881, 'Great game! Great Developers!!!')]



