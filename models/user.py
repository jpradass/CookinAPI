from typing import Dict, List
import uuid
from db import db
from werkzeug.security import check_password_hash

userJSON = Dict[str, str]

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(40), primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username: str, password: str) -> None:
        self.id = uuid.uuid4()
        self.username = username
        self.password = password
    
    def json(self) -> userJSON:
        return {'id': self.id, 'username': self.username}

    def check_pwd(self, pwd) -> bool:
        return check_password_hash(self.password, pwd)

    def saveto_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def deletefrom_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def findby_id(cls, _id) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def findby_username(cls, username) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def searchby_username(cls, username) -> List["UserModel"]:
        return cls.query.filter(cls.username.like(f"%{username}%")).all()

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.all()
