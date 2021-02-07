from typing import Dict, List, Union
from models.ingredient import IngredientModel
from db import db

RecipeJSON = Dict[str, Union[str, float, List]]

class RecipeModel(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    calories = db.Column(db.Float(precision=2))
    instructions = db.Column(db.String)

    ingredients = db.relationship("IngredientModel")

    def __init__(self, uuid: str, name: str, calories: float, instructions: str, ingredients: List) -> None:
        self.id = uuid
        self.name = name
        self.calories = calories
        self.instructions = instructions
        for ingredient in ingredients:
            self.ingredients.append(IngredientModel(ingredient['name'], ingredient['quantity'], self.id))

    def json(self) -> RecipeJSON:
        return {"id": self.id, "name": self.name, "calories": self.calories, "instructions": self.instructions, "ingredients": [ingredient.json() for ingredient in self.ingredients]}

    def saveto_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def deletefrom_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def search_by(cls, search_obj: Dict[str, str]) -> List["RecipeModel"]:
        if search_obj['key_search'] == 'name':
            return cls.searchby_name(search_obj['value_search'])
        elif search_obj['key_search'] == 'calories':
            return cls.searchby_calories(search_obj['value_search'])
        elif search_obj['key_search'] == 'instructions':
            return cls.searchby_instructions(search_obj['value_search'])
        else: return None

    @classmethod
    def searchby_name(cls, name: str) -> List["RecipeModel"]:
        return cls.query.filter(cls.name.ilike(f"%{name}%")).all()

    @classmethod
    def searchby_calories(cls, calories: float) -> List["RecipeModel"]:
        return cls.query.filter(cls.calories.ilike(f"%{calories}%")).all()

    @classmethod
    def searchby_instructions(cls, instructions: str) -> List["RecipeModel"]:
        return cls.query.filter(cls.instructions.ilike(f"%{instructions}%")).all()

    @classmethod
    def findby_id(cls, _id: str) -> "RecipeModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def search_all(cls) -> List["RecipeModel"]:
        return cls.query.all()