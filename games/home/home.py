from flask import Blueprint, render_template, session

## import utilities later

home_blueprint = Blueprint('home_bp',__name__)

@home_blueprint.route('/',methods = ['GET'])
def home():

    log_status = False
    user_authenticated = 'user_name' in session
    if (user_authenticated):
        log_status = True
    print(log_status)

    return render_template('home.html',
                           log_status = log_status)