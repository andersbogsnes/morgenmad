from flask import Blueprint, render_template, url_for, flash, redirect
from morgenmad.utils import confirm_token
from morgenmad.user.model import User
from morgenmad.extensions import db
from flask_login import login_required

user_blueprint = Blueprint('user', __name__, template_folder="templates", url_prefix='/user')


@user_blueprint.route('/profile')
@login_required
def profile():
    return render_template('users/profile.html')


@user_blueprint.route('/confirm/<token>')
def confirm(token):
    try:
        email = confirm_token(token)
    except:
        flash("Bekræftelsen er udløbet", "alert alert-danger")
        return redirect(url_for('public.login'))

    user = User.query.filter_by(email=email).first_or_404()

    if user.email_confirmed:
        flash("Allerede bekræftet - brug login", "alert alert-success")
        return redirect(url_for('public.login'))
    else:
        user.email_confirmed = True
        db.session.add(user)
        db.session.commit()
        flash("Du er nu bekræftet!", "alert alert-success")
    return redirect(url_for('user.profile'))