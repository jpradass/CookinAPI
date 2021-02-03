from typing import Dict, List, Union
import uuid

from db import db

IngredientJSON = Dict[str, Union[str, int]]

class IngredientModel(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(80))
    quantity = db.Column(db.Integer)
    
    recipe_id = db.Column(db.String(40), db.ForeignKey('recipes.id'), nullable=False)
    recipe = db.relationship("RecipeModel")

    def __init__(self, name: str, quantity: int, recipe_id: str) -> None:
        self.id = uuid.uuid4().__str__()
        self.name = name
        self.quantity = quantity
        self.recipe_id = recipe_id

    def json(self) -> IngredientJSON:
        return {"name": self.name, "quantity": self.quantity}

    def saveto_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def deletefrom_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def findby_name(cls, name) -> "IngredientModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def findby_id(cls, _id) -> "IngredientModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["IngredientModel"]:
        return cls.query.all()