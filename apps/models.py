import uuid
from .database import db

class Users(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    public_id   = db.Column(db.String(40), nullable=False)
    username    = db.Column(db.String(50), unique=True, nullable=False)
    password    = db.Column(db.String(300), nullable=False)

    def __init__(self, username, password) -> None:
        self.username   = username
        self.password   = password
        self.public_id  = str(uuid.uuid4())
        