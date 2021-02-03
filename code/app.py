from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from redis_access import revoked_store, ACCESS_EXPIRES, REFRESH_EXPIRES

from resources.recipe import Recipe, RecipeList
from resources.ingredient import Ingredient
from resources.user import UserList, UserLogin, UserLogout, TokenRefresh

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db" # For development purposes, when deployed it is recommended postgresql or some another
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = REFRESH_EXPIRES
app.secret_key = "josue"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def checktoken_revoked(decrypted_token):
    jti = decrypted_token['jti']
    entry = revoked_store.get(jti)
    if entry is None:
        return True
    return entry == 'true'

api.add_resource(Recipe, '/recipe/<string:uuid>')
api.add_resource(RecipeList, '/recipe')
api.add_resource(Ingredient, '/ingredient/<string:uuid>')
api.add_resource(UserLogin, '/auth/login')
api.add_resource(UserLogout, '/auth/logout')
api.add_resource(TokenRefresh, "/auth/refresh")
api.add_resource(UserList, '/user')

if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)