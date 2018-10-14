from flask import Blueprint, render_template

profile_app = Blueprint('profile', __name__, url_prefix='/profile')


@profile_app.route('/view')
def view():
    return render_template('user_view.html')
