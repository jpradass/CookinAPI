from typing import List
import uuid

from db import db

class IngredientModel(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.String(30), nullable=False)
    
    recipe_id = db.Column(db.String(40), db.ForeignKey('recipes.id'))
    recipe = db.relationship("RecipeModel")

    def __init__(self, name: str, quantity: int, recipe_id: str) -> None:
        self.id = uuid.uuid4().__str__()
        self.name = name
        self.quantity = quantity
        self.recipe_id = recipe_id

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