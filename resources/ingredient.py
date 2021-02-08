from flask_jwt_extended import jwt_required
from flask import request
from flask_restful import Resource
from models.ingredient import IngredientModel
from schemas.ingredient import IngredientSchema

ingredient_schema = IngredientSchema()

class Ingredient(Resource):
    @jwt_required
    def get(self):
        uuid = request.args.get('uuid')
        if not uuid:
            return {'message': 'missing uuid parameter'}, 400
            
        recipe = IngredientModel.findby_id(uuid)
        if recipe:
            return ingredient_schema.dump(recipe), 200
        return {'message': 'Ingredient not found', 'description': uuid}, 404
