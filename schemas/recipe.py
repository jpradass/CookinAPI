from ma import ma 
from models.recipe import RecipeModel
from schemas.ingredient import IngredientSchema

class RecipeSchema(ma.SQLAlchemyAutoSchema):
    ingredients = ma.Nested(IngredientSchema, many=True)

    class Meta:
        model = RecipeModel
        load_instance = True
        # load_only = ("password",)
        dump_only = ("id",)
        include_fk = True