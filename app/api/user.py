from flask import Blueprint, request, jsonify, abort
from flask.views import MethodView
from app.extensions import bcrypt
from app.model import User

user_api = Blueprint('user_api', __name__, url_prefix='/api')


class UserAPI(MethodView):
    def get(self, user_id, page=1):
        """Looks up single user if user_id is passed, else returns a json of all users"""
        if user_id is None:
            result = User.query.paginate(page, 10).items
        else:
            result = User.query.get_or_404(user_id)


        response = {res.id: {'navn': res.fullname,
                             'email': res.email,
                             'tlf_nr': res.tlf_nr} for res in result}

        return jsonify(response)

    def put(self):
        """Create a user given input data
        :param fornavn
        :param efternavn
        :param tlf_nr
        :param email
        :param password"""

        data = request.json


    def post(self):
        pass

    def delete(self):
        pass

user_view = UserAPI.as_view('user_view')
user_api.add_url_rule('/user', defaults={'user_id': None}, view_func=user_view, methods=['GET'])
user_api.add_url_rule('/user/<int:user_id>', view_func=user_view, methods=['GET'])

@user_api.errorhandler(404)
def data_error(error):
    return jsonify({"error": "404: Not Found"}), 404