from flask import Blueprint, render_template, session, redirect, url_for

import games.profile.services as services

import games.adapters.repository as repo
from games.authentication.authentication import login, login_required
from games.domainmodel.model import User, Review

profile_blueprint = Blueprint('profile_bp',__name__)


@profile_blueprint.route('/profile',methods = ['GET'])
@login_required
def profile():
    if 'user_name' in session:
        user_name = session['user_name']
        #print(user_name)


    user1 = services.get_user(repo.repository_instance,user_name)
    likedGames = services.get_liked_games_objects(repo.repository_instance, user1)
    print("profile")
    print(likedGames)
    return render_template('profile.html',user = user1,likedGames=likedGames )


@profile_blueprint.route('/profile/<int:gameID>',methods = ['GET'])
@login_required
def add_game(gameID):
    if 'user_name' in session:
        user_name = session['user_name']
        user = services.get_user(repo.repository_instance,user_name)
        game = services.get_game(repo.repository_instance,gameID)
        gameAdded = False;



        print("in profile.py")
        print(user)
        gameAdded = services.toggle_favourite(repo.repository_instance, game, user)
        if not gameAdded:
            gameAdded = False
        else:
            gameAdded = True


        title = game.title
        likedGames = services.get_liked_games_objects(repo.repository_instance,user)
        print(likedGames)

    return render_template('profile.html', user=user,gameAdded = gameAdded,title = title,likedGames = likedGames)



