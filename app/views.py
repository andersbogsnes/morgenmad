from flask import Blueprint, render_template

main_view = Blueprint('main', __name__, template_folder='templates')


@main_view.route('/')
def main():
    return render_template('main.html')


@main_view.app_errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404




