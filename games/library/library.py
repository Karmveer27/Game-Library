import math

from flask_wtf import FlaskForm
from flask import Blueprint,render_template, url_for, redirect,request, session
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, HiddenField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

import games.library.services as services
import games.adapters.repository as repo

## import utilities later
from games.authentication.authentication import login_required

library_blueprint = Blueprint('library_bp', __name__)
filter_by_genre_blueprint = Blueprint("filter_by_genre_bp", __name__)



@library_blueprint.route('/library/<int:page>', methods=['GET'])
@library_blueprint.route('/library/<string:genre_required>/<int:page>', methods=['GET'])
@library_blueprint.route('/library', methods=['GET'])

def library(page=1, genre_required = None):
    genres = services.get_genres(repo.repository_instance)
    if genre_required:
        games_list = services.games_of_specific_genre(repo.repository_instance, genre_required)
        games_list = sorted(games_list, key=lambda game_sorted: game_sorted.title)
    else:
        games_list = services.get_games(repo.repository_instance)
        games_list = sorted(games_list, key=lambda game_sorted: game_sorted['title'])



# def library(page=1):
#     genres = services.get_genres(repo.repository_instance)
#     games_list = services.get_games(repo.repository_instance)
#
#

    #alphabetically_sorted = sorted(games_list, key= lambda game_sorted: game_sorted['title'])

    per_page = 40  # Number of games per page
    #total_pages = (len(alphabetically_sorted) + per_page - 1) // per_page  # Calculate total pages
    #all_pages = math.ceil(len(alphabetically_sorted) / per_page)

    total_pages = (len(games_list) + per_page - 1) // per_page  # Calculate total pages
    all_pages = math.ceil(len(games_list) / per_page)

    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    #games_to_display = alphabetically_sorted[start_idx:end_idx]
    games_to_display = games_list[start_idx:end_idx]
    if page > 1:
        previous_page = page - 1
    else:
        previous_page = None

    if page < total_pages:
        next_page = page + 1
    else:
        next_page = None


    # Calculate pages to show before and after the current page
    prev_3_pages = range(max(1, page - 3), page)
    next_3_pages = range(page + 1, min(total_pages + 1, page + 4))

    user_authenticated = 'user_name' in session
    #print("in library.py")
   # print(user_authenticated)
    log_status = False;

    try:
        if(user_authenticated):
            log_status = True;
            user_name = session['user_name']
            user = services.get_user(repo.repository_instance,user_name)
            liked_games = services.get_liked_games(repo.repository_instance,user)

        else:
            liked_games = []
    except:
        liked_games = []


    #print("liked games")
    #print(liked_games)
    #print(log_status)
    return render_template('library.html',
                           games=games_to_display,
                           current_page=page,
                           prev_page=previous_page,
                           next_page=next_page,
                           prev_3_pages=prev_3_pages,
                           next_3_pages=next_3_pages,
                           last_page=all_pages,
                           genres = genres,
                           genre_required=genre_required,
                           user_authenticated=user_authenticated,
                           liked_games = liked_games,
                           log_status = log_status)



@library_blueprint.route('/library/game/<int:id>', methods=['GET'])
def game_detail(id):
    log_status = False;
    user_authenticated = 'user_name' in session
    if (user_authenticated):
        log_status = True;

    game = services.get_game_by_id(id, repo.repository_instance)

    average_rating = services.get_average_rating(id, repo.repository_instance)
    print("average rating")
    print(average_rating)
    return render_template('gameDescription.html', game=game,log_status = log_status, average_rating=average_rating)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired("Your review is required"),
        Length(min=4, message='Your review is too short')])

    rating = IntegerField('Rating', [
        DataRequired("Your rating between 1-5 is required"), NumberRange(min=0, max=5, message="Your rating must be an Integer between 0 and 5")])

    game_id = HiddenField("Game id")
    submit = SubmitField('Submit')


@library_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_game():
    user_name = session['user_name']

    form = ReviewForm()

    if form.validate_on_submit():

        game_id = form.game_id.data


        services.add_review(game_id, form.review.data, form.rating.data, user_name, repo.repository_instance)

            #return redirect(url_for('authentication_bp.logout'))

        game = services.get_game_by_id(game_id, repo.repository_instance)

        return redirect(url_for('library_bp.game_detail', id=game_id))

    if request.method == 'GET':
        #UNSURE ABOUT THIS LINE!!!!!!!!!!!

        game_id = request.args.get('game_id')
        form.game_id.data = game_id

    else:
        game_id = form.game_id.data

    game = services.get_game_by_id(game_id, repo.repository_instance)

    return render_template(
        'comment_on_game.html',
        form=form,
        game=game,
        handler_url=url_for('library_bp.review_game'))











# @library_blueprint.route('/library/genre/<string:genreName>', methods=['GET'])
# def game_genres(genreName):
#
#
#     return render_template('genre_Navigation.html', )
#
# @filter_by_genre_blueprint.route('/library/<string:genre_required>/<int:page>', methods=['GET'])
# @filter_by_genre_blueprint.route('/library/<int:page>', methods=['GET'])
# @filter_by_genre_blueprint.route('/library', methods=['GET'])
# def filter_by_genre(page=1, genre_required = None):
#
#     games_list = services.games_of_specific_genre(repo.repository_instance, genre_required)
#     alphabetically_sorted = sorted(games_list, key= lambda game_sorted: game_sorted['title'])
#
#     per_page = 40  # Number of games per page
#     total_pages = (len(alphabetically_sorted) + per_page - 1) // per_page  # Calculate total pages
#     all_pages = math.ceil(len(alphabetically_sorted) / per_page)
#     if page < 1:
#         page = 1
#     elif page > total_pages:
#         page = total_pages
#
#     start_idx = (page - 1) * per_page
#     end_idx = start_idx + per_page
#     games_to_display = alphabetically_sorted[start_idx:end_idx]
#
#     if page > 1:
#         previous_page = page - 1
#     else:
#         previous_page = None
#
#     if page < total_pages:
#         next_page = page + 1
#     else:
#         next_page = None
#
#
#     # Calculate pages to show before and after the current page
#     prev_3_pages = range(max(1, page - 3), page)
#     next_3_pages = range(page + 1, min(total_pages + 1, page + 4))
#
#     return render_template('genre_Navigation.html',
#                            games=games_to_display,
#                            current_page=page,
#                            prev_page=previous_page,
#                            next_page=next_page,
#                            prev_3_pages=prev_3_pages,
#                            next_3_pages=next_3_pages,
#                            last_page=all_pages)
#
