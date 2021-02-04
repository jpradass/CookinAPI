from flask_jwt_extended import jwt_required
from flask_restful import Resource
from models.ingredient import IngredientModel

class Ingredient(Resource):
    @jwt_required
    def get(self, uuid):
        recipe = IngredientModel.findby_id(uuid)
        if recipe:
            return recipe.json()
        return {'message': 'Ingredient not found', 'description': uuid}, 404
