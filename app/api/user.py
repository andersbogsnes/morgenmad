from flask import Blueprint, request, jsonify, abort
from flask.views import MethodView
from app.model import User, UserSchema
from flask_login import login_required
from app.extensions import csrf, db
from sqlalchemy.orm.exc import NoResultFound

user_api = Blueprint('user_api', __name__, url_prefix='/api')


class UserAPI(MethodView):
    decorators = [login_required, csrf.exempt]

    def get(self, user_id, page=1):
        """Looks up single user if user_id is passed, else returns a json of all users"""
        user_schema = UserSchema(only=('id', 'fullname', 'email'))
        users_schema = UserSchema(only=('id', 'fullname', 'email'), many=True)
        if user_id is None:
            return users_schema.jsonify(User.query.all())
        else:
            return user_schema.jsonify(User.query.get_or_404(user_id))

    def put(self, user_id):
        """Updates an existing user
        :param fornavn
        :param efternavn
        :param tlf_nr
        :param email
        :param password"""

        data = request.json
        if not data:
            abort(404)

        user_schema = UserSchema(partial=True)

        errors = user_schema.validate(data)

        if errors:
            return jsonify(errors), 422
        try:
            db.session.query(User).filter_by(id=user_id).one()
            db.session.query(User).filter_by(id=user_id).update(data)
            db.session.commit()
            return jsonify(dict(success="User updated")), 201
        except NoResultFound:
            return jsonify(dict(error="User not found")), 404

    def post(self):
        """Create a user given input data
        :param fornavn
        :param efternavn
        :param tlf_nr
        :param email
        :param password"""

        data = request.json
        user_schema = UserSchema(only=('fornavn', 'efternavn', 'tlf_nr', 'email', 'password'))

        user, errors = user_schema.load(data)
        if errors:
            return jsonify(errors), 422
        db.session.add(user)
        db.session.commit()
        return jsonify(dict(success="User created"))

    def delete(self):
        pass


user_view = UserAPI.as_view('user_view')
user_api.add_url_rule('/user', defaults={'user_id': None}, view_func=user_view, methods=['GET'])
user_api.add_url_rule('/user/<int:user_id>', view_func=user_view, methods=['GET', 'PUT'])
user_api.add_url_rule('/user', view_func=user_view, methods=['POST'])


@user_api.errorhandler(404)
def data_error(error):
    return jsonify({"error": "404: Not Found"}), 404
