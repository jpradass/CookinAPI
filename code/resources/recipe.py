from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.recipe import RecipeModel

class Recipe(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be left blank", location='json'
    )
    parser.add_argument(
        "calories", type=float, required=True, help="Every recipe has its calories", location='json'
    )
    parser.add_argument(
        "instructions", type=str, required=True, help="Every recipe needs its instructions", location='json'
    )
    parser.add_argument(
        "ingredients", type=list, required=True, help="Every recipe has a way to be done", location='json'
    )

    @jwt_required
    def get(self, uuid):
        recipe = RecipeModel.findby_id(uuid)
        if recipe:
            return recipe.json()
        return {'message': "Recipe not found", 'description': uuid}, 404

    @jwt_required
    def post(self, uuid):
        if RecipeModel.findby_id(uuid):
            return {'message': "Recipe with this uuid already exists", 'description': uuid}, 400
        
        data = Recipe.parser.parse_args()
        recipe = RecipeModel(uuid, **data)

        recipe.saveto_db()
        return {'recipe': recipe.json()}, 201

class RecipeList(Resource):
    @jwt_required
    def get(self):
        return {'recipes': [recipe.json() for recipe in RecipeModel.find_all()]}
