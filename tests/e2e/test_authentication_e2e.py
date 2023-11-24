import pytest
from flask import session


# Test Registration, Login, and Logout========================================================================================================

def test_register_login_logout(client):
    # Register a new user.
    client.post('/authentication/register', data={'user_name': 'testuser', 'password': 'Test1234'})

    # Login the user.
    client.post('/authentication/login', data={'user_name': 'testuser', 'password': 'Test1234'})
    assert 'user_name' in session

    # Logout the user.
    client.get('/authentication/logout')
    assert 'user_name' not in session

# Registration with invalid Input=====================================================================================================
@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('testuser', 'Test#6^0', b'Your user name is already taken - please supply another'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    client.post('/authentication/register', data={'user_name': 'testuser', 'password': 'Test1234'})
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data




# Test Browsing Games========================================================================================================
def test_browse_games(client):
    # Simulate browsing games.
    response = client.get('/library')

    # Check if the games are displayed correctly.
    assert b'10 Second Ninja X' in response.data
    assert b'100 Doors: Escape from Work' in response.data

    # Navigate to a game details page.
    response = client.get('/library/game/435790')
    assert b'10 Second Ninja X' in response.data

# Test Adding Game to Wishlist========================================================================================================
def test_add_game_to_wishlist(client,auth):

    client.post('/authentication/register', data={'user_name': 'testuser', 'password': 'Test1234'})
    client.post('/authentication/login', data={'user_name': 'testuser', 'password': 'Test1234'})
    # Add a game to the user's wishlist.
    response = client.get('/profile/1109350')


    # Check if the game is displayed on the wishlist page.
    assert b'ANCIENT SOULS : The Governor has been added to your favorite list!' in response.data

# Test Searching Games========================================================================================================
def test_search_games(client):
    # Simulate searching for games.
    response = client.get('/search?search_query=ca&search_category=title')

    # Check if search results match the query.

    assert b'Call of Duty' in response.data
    assert b'4: Modern Warfare' in response.data
    assert b'Farm Frenzy 3: American Pie' in response.data

# test index========================================================================================================
def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Silent Artifact' in response.data

#=================Comments ===================================================================

def test_login_required_to_comment(client):
    # Try to post comment on review without being logged in
    response = client.post('/review?game_id=435790')
    # Client should get redirected to login page
    assert response.status_code == 302
    assert '/authentication/login' in response.headers['Location']


def test_comment(client):
    # Login a user.
    client.post('/authentication/register', data={'user_name': 'testuser', 'password': 'Test1234'})
    client.post('/authentication/login', data={'user_name': 'testuser', 'password': 'Test1234'})


    game_id = 435790

    # Attempt to review the game.
    response = client.post(
        '/review',
        data={'game_id': game_id, 'review': "Bad Game", 'rating': 2}
    )

    assert '/library/game/435790' in response.headers['Location']


@pytest.mark.parametrize(('review_text', 'rating', 'messages'), (
        ('Who thinks this game is awesome?', 5, ()),
        ('Hey', 3, ()),
        ('Good game', 6, (b'Your rating must be an Integer between 0 and 5',)),
))
def test_review_game_with_invalid_input(client, auth, review_text, rating, messages):
    # Login a user.
    client.post('/authentication/register', data={'user_name': 'testuser', 'password': 'Test1234'})
    client.post('/authentication/login', data={'user_name': 'testuser', 'password': 'Test1234'})


    game_id = 435790

    # Attempt to review the game.
    response = client.post(
        '/review',
        data={'game_id': game_id, 'review': review_text, 'rating': rating}
    )

    # Check that supplying invalid review text or rating generates appropriate error messages.
    for message in messages:
        assert message in response.data