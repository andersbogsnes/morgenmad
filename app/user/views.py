from flask import Blueprint, render_template, url_for, flash, redirect, g
from app.utils import confirm_token, generate_confirmation_token, send_confirmation_email
from app.model import User
from app.user.forms import SignupForm, LoginForm
from app.extensions import db, login_manager
from flask_login import login_user, logout_user, login_required, current_user

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            redirect(url_for('user.profile'))
        else:
            flash("Forkert bruger og/eller passord", category="alert alert-danger")
            redirect(url_for('user.login'))
    return render_template('user/login.html', form=form)


@user_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            return render_template("user/signup.html", error="Email findes allerede", form=form)
        user = User(fornavn=form.firstname.data,
                    efternavn=form.lastname.data,
                    tlf_nr=form.tlf_nr.data,
                    email=form.email.data,
                    password=form.password.data
                    )
        print(user.id)
        db.session.add(user)
        db.session.commit()
        token = generate_confirmation_token(form.email.data)
        confirm_url = url_for('user.confirm', token=token, _external=True)
        html = render_template("user/confirmation_email.html", confirm_url=confirm_url)
        send_confirmation_email(form.email.data, "KSM email bekræftelse", html)

        flash("Vi har sendt dig en bekræftelsesmail!", category="alert alert-success")
        login_user(user)
        return redirect(url_for('user.profile'))

    return render_template("user/signup.html", form=form)


@user_blueprint.route('/profile')
@login_required
def profile():
    return render_template('user/profile.html')

@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Du er nu logget ud", category="alert alert-warning")
    return redirect(url_for('main.main'))


@user_blueprint.route('/confirm/<token>')
def confirm(token):
    try:
        email = confirm_token(token)
    except:
        flash("Bekræftelsen er udløbet", "alert alert-danger")
    user = User.query.filter_by(email=email).first_or_404()
    if user.email_confirmed:
        flash("Allerede bekræftet - brug login", "alert alert-success")
    else:
        user.email_confirmed = True
        db.session.add(user)
        db.session.commit()
        flash("Du er nu bekræftet!", "alert alert-success")
    return redirect(url_for('user.profile'))


@user_blueprint.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


login_manager.login_view = 'user.login'
