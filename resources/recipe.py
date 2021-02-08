from flask_jwt_extended import jwt_required
from flask import request
from flask_restful import Resource
from models.recipe import RecipeModel
from schemas.recipe import RecipeSchema

recipe_schema = RecipeSchema()
recipe_list_schema = RecipeSchema(many=True)

class Recipe(Resource):
    @jwt_required
    def get(self):
        uuid = request.args.get("uuid")
        if not uuid:
            return {'message': "Missing uuid parameter", 'description': {'search_key': 'uuid', 'search_value': uuid}}, 404

        recipe = RecipeModel.findby_id(uuid)
        if recipe:
            return recipe_schema.dump(recipe), 200
        return {'message': "Recipe not found", 'description': uuid}, 404

    @jwt_required
    def post(self):        
        recipe = RecipeModel(**request.get_json())
        if RecipeModel.findby_name(recipe.name):
            return {'message': "Recipe with this name '{}' already exists".format(recipe.name)}, 400

        recipe.saveto_db()
        return {'recipe': recipe_schema.dump(recipe)}, 201

    @jwt_required
    def put(self):
        recipe_data = recipe_schema.load(request.get_json())

        recipe = RecipeModel.findby_name(recipe_data.name)
        if not recipe:
            return {'message': "Recipe not found", 'description': recipe_data.name}, 404

        if recipe_data.name: recipe.name = recipe_data.name
        if recipe_data.calories: recipe.calories = recipe_data.calories        
        if recipe_data.instructions: recipe.instructions = recipe_data.instructions

        recipe.saveto_db()
        return {'recipe': recipe_schema.dump(recipe)}, 200

    @jwt_required
    def delete(self):
        uuid = request.args.get('uuid')
        if not uuid:
            return {'message': "Missing uuid parameter", 'description': {'search_key': 'uuid', 'search_value': uuid}}, 404
        
        recipe = RecipeModel.findby_id(uuid)
        if recipe:
            recipe.deletefrom_db()
            return {'message': 'Recipe deleted', 'description': uuid}
        return {'message': 'Recipe not found', 'description': uuid}, 404

class RecipeList(Resource):
    @jwt_required
    def get(self):
        recipes = RecipeModel.search_all()
        return {'items': len(recipes), 'recipes': recipe_list_schema.dump(recipes)}

class RecipeSearch(Resource):
    def get(self):
        search_obj = {'key_search': None, 'value_search': None}
        name, calories, instructions = request.args.get('name'), request.args.get('calories'), request.args.get('instructions')
        if name:
            search_obj['key_search'] = 'name'
            search_obj['value_search'] = name
        elif calories: 
            search_obj['key_search'] = 'calories'
            search_obj['value_search'] = calories
        elif instructions: 
            search_obj['key_search'] = 'instructions'
            search_obj['value_search'] = instructions

        recipes = RecipeModel.search_by(search_obj)
        if recipes:
            return {'items': len(recipes),'recipes': recipe_list_schema.dump(recipes)}
        return {'message': 'Search did not found a recipe', 'description': search_obj}, 404
