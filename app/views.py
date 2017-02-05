from flask import Blueprint, render_template
from app.model import Morgenmad
from app.extensions import db
import datetime
main_view = Blueprint('main', __name__, template_folder='templates')


@main_view.route('/')
def main():
    today = datetime.date.today()
    twenty_days = datetime.timedelta(days=10)
    fridays = (db.session.query(Morgenmad)
               .filter(Morgenmad.dato.between((today-twenty_days),
                                              (today+twenty_days))))

    return render_template('main.html', data=fridays)


@main_view.app_errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404




