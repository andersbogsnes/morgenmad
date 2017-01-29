from flask import Blueprint, render_template, request, flash
from app.forms import SignupForm
from app.model import User
from app.extensions import db

main_view = Blueprint('main', __name__, template_folder='static/templates')


@main_view.route('/')
def main():
    return render_template('main.html')


@main_view.route('/signup', methods=['GET', 'POST'])
def login():
    form = SignupForm()

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            return render_template("signup.html", error="Email findes allerede", form=form)
        user = User(fornavn=form.firstname.data,
                    efternavn=form.lastname.data,
                    tlf_nr=form.tlf_nr.data,
                    email=form.email.data,
                    password=form.password.data
                    )
        db.session.add(user)
        db.session.commit()
        flash("Bruger er nu oprettet", category="alert alert-success")

    return render_template("signup.html", form=form)


@main_view.app_errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
