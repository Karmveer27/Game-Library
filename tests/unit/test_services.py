import pytest
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre
import games.library.services as library_services
import games.browse.services as browse_services
from tests.conftest import in_memory_repo

repo = in_memory_repo

def test_get_number_of_games(repo):


    # Call the function to get the number of games
    result = browse_services.get_number_of_games(repo)

    expected_number_of_games = 877
    assert result == expected_number_of_games

def test_get_games(repo):

    # Call the function to get the list of games
    all_games = library_services.get_games(repo)

    first_game = all_games[:1]

    assert first_game[0]['game_id'] == 3010





def test_get_game_by_id(repo):

    # Call the function to get a game by its ID
    # Game_id for Call Of Duty Used (7940)
    result = library_services.get_game_by_id(7940, repo)

    # Replace expected_game with the expected result
    expected_game = repo.get_game_by_id(7940)
    assert result == expected_game

def test_get_genres(repo):


    # Call the function to get the list of genres
    result = library_services.get_genres(repo)
    print(result)

    expected_genre_names = ['Action', 'Adventure', 'Animation & Modeling', 'Audio Production', 'Casual', 'Design & Illustration', 'Early Access', 'Education', 'Free to Play', 'Game Development', 'Gore', 'Indie', 'Massively Multiplayer', 'Photo Editing', 'RPG', 'Racing', 'Simulation', 'Software Training', 'Sports', 'Strategy', 'Utilities', 'Video Production', 'Violent', 'Web Publishing']
    assert result == expected_genre_names

def test_is_game_of_genre_with_matching_genre(in_memory_repo):


    #Getting the Game Call of Duty Which is Expected to have the genre of 'Action'
    game = in_memory_repo.get_game_by_id(7940)

    # Call the function to check if the game has the required genre
    result = library_services.is_game_of_genre(game, 'Action')

    # The game should match the required genre
    assert result is True

def test_is_game_of_genre_with_non_matching_genre(in_memory_repo):

    #Getting the Game Call of Duty Which is Expected to have the genre of 'Action'
    game = in_memory_repo.get_game_by_id(7940)

    # Call the function to check if the game has the required genre, it is expected to output False
    result = library_services.is_game_of_genre(game, 'Fantasy')

    # The game should not match the required genre
    assert result is False

