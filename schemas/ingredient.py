from ma import ma 
from models.ingredient import IngredientModel

class IngredientSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = IngredientModel
        load_instance = True
        load_only = ("recipe_id","id")
        # dump_only = ("id",)
        include_fk = True