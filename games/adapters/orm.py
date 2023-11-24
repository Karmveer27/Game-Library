from sqlalchemy import Column, Integer, Table, String, Float, Date, ForeignKey, Text, DateTime, MetaData
from sqlalchemy.orm import registry, relationship, mapper

from games.domainmodel.model import User, Review, Publisher, Game, Genre, Wishlist


metadata = MetaData()


users_table = Table(
    'users', metadata,
    Column('user_id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255),unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)


publishers_table = Table(
    'publishers', metadata,
    Column('name', String(255), primary_key=True)
)


games_table = Table(
    'games', metadata,
    Column('game_id', Integer, primary_key=True),
    Column('game_title', Text, nullable=True),
    Column('game_price', Float, nullable=True),
    Column('release_date', String(50), nullable=True),
    Column('game_description', String(255), nullable=True),
    Column('game_image_url', String(255), nullable=True),
    Column('video_url', String(255), nullable=True),
    Column('game_website_url', String(255), nullable=True),
    Column('publisher_name', ForeignKey('publishers.name'))
)


genres_table = Table(
    'genres', metadata,
    Column('genre_name', String(64), primary_key=True, nullable=False)
)


reviews_table = Table(
    'reviews', metadata,
    Column('review_id', Integer, primary_key=True, autoincrement=True),
    # Column('timestamp', DateTime, nullable=False),

    Column('review_text', String(255), nullable=False),
    Column('rating', Integer, nullable=False),

    Column('game_id', Integer, ForeignKey('games.game_id')),
    Column('user_id', Integer, ForeignKey('users.user_id')),

)

game_genres_table = Table(
    'game_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),

    Column('game_id', ForeignKey('games.game_id')),
    Column('genre_name', ForeignKey('genres.genre_name'))
)



wishlists_table = Table(
    'wishlist', metadata,
    Column('wishlist_id', Integer, primary_key=True, autoincrement=True),
    Column('user_id',Integer,  ForeignKey('users.user_id')),
    Column('username',String(255))
)

game_wishlist_table = Table(
    'game_wishlist', metadata,
    Column('id', Integer, primary_key=True,autoincrement=True),
    Column('game_id', ForeignKey('games.game_id')),
    Column('wishlist_id',ForeignKey('wishlist.wishlist_id')),

)


def map_model_to_tables():
    mapper(User, users_table, properties={
        '_User__user_id': users_table.c.user_id,
        '_User__username': users_table.c.username,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(Review, back_populates='_Review__user')
    })

    mapper(Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.name
    })

    mapper(Game, games_table, properties={
        '_Game__game_id': games_table.c.game_id,
        '_Game__game_title': games_table.c.game_title,
        '_Game__price': games_table.c.game_price,
        '_Game__release_date': games_table.c.release_date,
        '_Game__description': games_table.c.game_description,
        '_Game__image_url': games_table.c.game_image_url,
        '_Game__website_url': games_table.c.game_website_url,
        '_Game__publisher': relationship(Publisher),
        '_Game__reviews': relationship(Review, back_populates='_Review__game'),
        '_Game__genres': relationship(Genre, secondary=game_genres_table),
    })

    mapper(Review, reviews_table, properties={
        # '_Review__timestamp': reviews_table.c.timestamp,
        '_Review__comment': reviews_table.c.review_text,
        '_Review__rating': reviews_table.c.rating,
        '_Review__user': relationship(User, back_populates='_User__reviews'),
        '_Review__game': relationship(Game, back_populates='_Game__reviews')
    })

    mapper(Wishlist, wishlists_table, properties={
        '_Wishlist_user': wishlists_table.c.user_id,
        '_Wishlist_username': wishlists_table.c.username,
        '_Wishlist__list_of_games': relationship(Game, secondary=game_wishlist_table)
    })

    mapper(Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.genre_name,
    })

