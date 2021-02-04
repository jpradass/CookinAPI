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
    def findby_name(cls, name) -> "RecipeModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def findby_id(cls, _id) -> "RecipeModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["RecipeModel"]:
        return cls.query.all()