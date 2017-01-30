from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.forms import SignupForm
from app.model import User
from app.extensions import db, login_manager
from app.utils import generate_confirmation_token, confirm_token, send_confirmation_email
from flask_login import login_required

main_view = Blueprint('main', __name__, template_folder='static/templates')


@main_view.route('/')
def main():
    return render_template('main.html')


@main_view.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main_view.route('/signup', methods=['GET', 'POST'])
def signup():
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
        token = generate_confirmation_token(form.email.data)
        confirm_url = url_for('main.confirm', token=token, _external=True)
        html = render_template('confirmation_email.html', confirm_url=confirm_url)
        send_confirmation_email(form.email.data, "KSM email bekræftelse", html)

        flash("Vi har sendt dig en bekræftelsesmail!", category="alert alert-success")
        return redirect(url_for('main.profile'))

    return render_template("signup.html", form=form)


@main_view.route('/confirm/<token>')
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
    return redirect(url_for('main.profile'))


@main_view.app_errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

login_manager.login_view = 'main.main'