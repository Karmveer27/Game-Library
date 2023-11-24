import math

from flask import Blueprint, render_template, url_for, redirect, request, session
import games.library.services as services
import games.adapters.repository as repo

## import utilities later

search_blueprint = Blueprint('search_bp', __name__)
filter_by_genre_blueprint = Blueprint("filter_by_genre_bp", __name__)


@search_blueprint.route('/search/<int:page>', methods=['GET'])
@search_blueprint.route('/search/<string:genre_required>/<int:page>', methods=['GET'])
@search_blueprint.route('/search', methods=['GET'])
def search(page=1, genre_required=None):
    search_query = request.args.get('search_query')
    search_category = request.args.get('search_category')

    genres = services.get_genres(repo.repository_instance)

    if search_category == 'title':
        searched_games = [game_dict for game_dict in services.get_games(repo.repository_instance) if
                          search_query.lower() in game_dict['title'].lower()]
    elif search_category == 'publisher':
        searched_games = [game_dict for game_dict in services.get_games(repo.repository_instance) if
                          game_dict['publisher'] and search_query.lower() in game_dict['publisher'].lower()]
    elif search_category == 'genre':
        searched_games = [game_dict for game_dict in services.get_games(repo.repository_instance) if
                          'genre' in game_dict and any(search_query.lower() in genre.genre_name.lower() for genre in game_dict['genre'])]
    else:
        searched_games = []

    per_page = 40
    total_pages = (len(searched_games) + per_page - 1) // per_page

    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    games_to_display = searched_games[start_idx:end_idx]

    if page > 1:
        previous_page = page - 1
    else:
        previous_page = None

    if page < total_pages:
        next_page = page + 1
    else:
        next_page = None

    prev_3_pages = range(max(1, page - 3), page)
    next_3_pages = range(page + 1, min(total_pages + 1, page + 4))
    log_status = False
    user_authenticated = 'user_name' in session
    if (user_authenticated):
        log_status = True

    return render_template('library.html',
                           games=games_to_display,
                           current_page=page,
                           prev_page=previous_page,
                           next_page=next_page,
                           prev_3_pages=prev_3_pages,
                           next_3_pages=next_3_pages,
                           last_page=total_pages,
                           genres=genres,
                           genre_required=genre_required,
                           log_status = log_status)





