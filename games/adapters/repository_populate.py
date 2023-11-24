import os.path
from pathlib import Path

from games.adapters.repository import AbstractRepository
from games.adapters.datareader.csvdatareader import GameFileCSVReader



def populate(data_path: Path, repo: AbstractRepository, database_mode: bool= False):
    dir_name = os.path.dirname(os.path.abspath(__file__))

    if database_mode:
        games_file_name = str(Path(data_path) / "games.csv")
    else:
        games_file_name = str(Path(data_path) / "games.csv")

    reader = GameFileCSVReader(games_file_name)
    reader.read_csv_file()

    publishers = reader.dataset_of_publishers
    games = reader.dataset_of_games
    genres = reader.dataset_of_genres

    
    print(genres)
    for publisher in publishers:
        repo.add_publisher(publisher)

    for genre in genres:
        repo.add_genre(genre)

    # Add above to the repo
    for game in games:
        repo.add_game(game)




