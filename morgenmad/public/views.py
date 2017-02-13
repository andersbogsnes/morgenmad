from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
import datetime

from morgenmad.extensions import login_manager
from morgenmad.public.forms import LoginForm
from morgenmad.user.forms import SignupForm
from morgenmad.user.model import User, Morgenmad
from morgenmad.extensions import db

public = Blueprint('public', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@public.route('/')
def main():
    today = datetime.date.today()
    twenty_days = datetime.timedelta(days=20)
    fridays = (db.session.query(Morgenmad)
               .filter(Morgenmad.dato.between(today - twenty_days,
                                              today + twenty_days))
               .order_by(Morgenmad.dato))

    return render_template('main.html', data=fridays)


@public.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash("Du er nu logget ind", category="alert alert-success")
            return redirect(url_for('user.profile'))
    return render_template('public/login.html', form=form)


@public.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Du er nu logget ud", category="alert alert-success")
    return redirect(url_for('public.main'))


@public.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if form.validate_on_submit():
        user = User(fornavn=form.firstname.data,
                    efternavn=form.lastname.data,
                    email=form.email.data,
                    password=form.password.data,
                    tlf_nr=form.tlf_nr.data)
        db.session.add(user)
        db.session.commit()
        flash("Tak for registreringen. Vi har sendt dig en bekræftelsesmail", category="alert alert-success")
        return redirect(url_for('public.main'))
    return render_template('public/signup.html', form=form)
