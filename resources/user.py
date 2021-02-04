from flask_jwt_extended.utils import get_raw_jwt
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    get_jwt_identity, 
    jwt_refresh_token_required,
    get_jti
)
from models.user import UserModel
from redis_access import revoked_store, ACCESS_EXPIRES, REFRESH_EXPIRES

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "username", type=str, required=True, help="This field cannot be left blank"
)
_user_parser.add_argument(
    "password", type=str, required=True, help="This field cannot be left blank"
)

class User(Resource):
    @jwt_required
    def get(self, username):
        user = UserModel.findby_username(username)
        if user:
            return user.json()
        return {'message': 'User not found', 'description': username}, 404

class UserList(Resource):
    @jwt_required
    def get(self):
        return {'users': [user.json() for user in UserModel.find_all()]}

class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.findby_username(data['username'])
        if user and user.check_pwd(data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            access_jti = get_jti(encoded_token=access_token)
            refresh_jti = get_jti(encoded_token=refresh_token)
            revoked_store.set(access_jti, 'false', ACCESS_EXPIRES)
            revoked_store.set(refresh_jti, 'false', REFRESH_EXPIRES)

            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        
        return {"message": "Invalid credentials", 'description': data['username']}, 401

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        revoked_store.set(jti, 'true', ACCESS_EXPIRES)
        return {"message": "User logout successfully"}

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        access_jti = get_jti(encoded_token=new_token)
        revoked_store.set(access_jti, 'false', REFRESH_EXPIRES)

        return {"access_token": new_token}
