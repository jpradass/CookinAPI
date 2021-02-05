from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.recipe import RecipeModel

opt_parser = reqparse.RequestParser()
opt_parser.add_argument(
    "name", type=str, required=False, help="This field cannot be left blank", location=['args', 'json']
)
opt_parser.add_argument(
    "calories", type=float, required=False, help="Every recipe has its calories", location=['args', 'json']
)
opt_parser.add_argument(
    "instructions", type=str, required=False, help="Every recipe needs its instructions", location=['args', 'json']
)
opt_parser.add_argument(
    "ingredients", type=list, required=False, help="Every recipe has a way to be done", location=['args', 'json']
)

class Recipe(Resource):
    @jwt_required
    def get(self, uuid):
        recipe = RecipeModel.findby_id(uuid)
        if recipe:
            return recipe.json()
        return {'message': "Recipe not found", 'description': uuid}, 404

    @jwt_required
    def post(self, uuid):
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

        if RecipeModel.findby_id(uuid):
            return {'message': "Recipe with this uuid already exists", 'description': uuid}, 400
        
        data = parser.parse_args()
        recipe = RecipeModel(uuid, **data)

        recipe.saveto_db()
        return {'recipe': recipe.json()}, 201

    @jwt_required
    def put(self, uuid):
        
        recipe = RecipeModel.findby_id(uuid)
        if not recipe:
            return {'message': 'Recipe not found', 'description': uuid}, 404

        data = opt_parser.parse_args()

        if data['name']: recipe.name = data['name']
        if data['calories']: recipe.calories = data['calories']
        if data['instructions']: recipe.instructions = data['instructions']

        recipe.saveto_db()
        return recipe.json() 

    @jwt_required
    def delete(self, uuid):
        recipe = RecipeModel.findby_id(uuid)

        if recipe:
            recipe.deletefrom_db()
            return {'message': 'Recipe deleted', 'description': uuid}

        return {'message': 'Recipe not found', 'description': uuid}, 404

class RecipeList(Resource):
    @jwt_required
    def get(self):
        recipes = RecipeModel.search_all()
        return {'items': len(recipes), 'recipes': [recipe.json() for recipe in recipes]}

class RecipeSearch(Resource):
    def get(self):
        search_obj = {'key_search': None, 'value_search': None}
        data = opt_parser.parse_args()

        if data['name']: 
            search_obj['key_search'] = 'name'
            search_obj['value_search'] = data['name']
        elif data['calories']: 
            search_obj['key_search'] = 'calories'
            search_obj['value_search'] = data['calories']
        elif data['instructions']: 
            search_obj['key_search'] = 'instructions'
            search_obj['value_search'] = data['instructions']

        recipes = RecipeModel.search_by(search_obj)
        if recipes:
            return {'items': len(recipes),'recipes': [recipe.json() for recipe in recipes]}
        return {'message': 'Search did not found a recipe', 'description': search_obj}, 404
