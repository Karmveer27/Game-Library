"""Initialize Flask app."""

from pathlib import Path

from _testcapi import test_config
from flask import Flask, render_template, session
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import clear_mappers, sessionmaker
from sqlalchemy.pool import NullPool

import games.adapters.repository as repo
from games.adapters import memory_repository, repository_populate, database_repository
from games.adapters.memory_repository import MemoryRepository
from games.adapters.memory_repository import populate

from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.adapters.orm import map_model_to_tables, metadata

# TODO: Access to the games should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
from games.domainmodel.model import Game


# TODO: Access to the games should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!

def create_some_game():
    filereader = GameFileCSVReader("games/adapters/data/games.csv")
    filereader.read_csv_file()
    listOfGames = filereader.dataset_of_games


    some_game = listOfGames[69]
    return some_game


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.


    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('games') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']
        print("ITES WORHHKIN")

        # Build the application - these steps require an application context.

    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repository_instance = memory_repository.MemoryRepository()
        # fill the content of the repository from the provided csv files (has to be done every time we start app!)
        database_mode = False
        repository_populate.populate(data_path, repo.repository_instance, database_mode)

    elif app.config['REPOSITORY'] == 'database':
        # Configure database.
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']

        # We create a comparatively simple SQLite database, which is based on a single file (see .env for URI).
        # For example the file database could be located locally and relative to the application in covid-19.db,
        # leading to a URI of "sqlite:///covid-19.db".
        # Note that create_engine does not establish any actual DB connection directly!
        database_echo = app.config['SQLALCHEMY_ECHO']
        # Please do not change the settings for connect_args and poolclass!
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo.repository_instance = database_repository.SqlAlchemyRepository(session_factory)

        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            print("getting to create all database engine")
            metadata.create_all(database_engine)  # Conditionally create database tables.
            for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                database_engine.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            database_mode = True
            repository_populate.populate(data_path, repo.repository_instance, database_mode)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

    with app.app_context():
        # Register blueprints.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .library import library
        app.register_blueprint(library.library_blueprint)
        app.register_blueprint(library.filter_by_genre_blueprint)

        from .search import search
        app.register_blueprint(search.search_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .profile import profile
        app.register_blueprint(profile.profile_blueprint)


       # from .news import news
       # app.register_blueprint(news.news_blueprint)

       # from .authentication import authentication
       # app.register_blueprint(authentication.authentication_blueprint)

       # from .utilities import utilities
       # app.register_blueprint(utilities.utilities_blueprint)

        # Register a callback the makes sure that database sessions are associated with http requests
        # We reset the session inside the database repository before a new flask request is generated
        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repository_instance, database_repository.SqlAlchemyRepository):
                repo.repository_instance.reset_session()

        # Register a tear-down method that will be called after each request has been processed.
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repository_instance, database_repository.SqlAlchemyRepository):
                repo.repository_instance.close_session()

    return app
