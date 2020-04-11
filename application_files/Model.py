# Model, consist of all the model classes such as points in db
from application_files import db


class Points(db.Model):
    # ID = KEY of a point
    id = db.Column(db.Integer, primary_key=True)
    # The point coordinates,represented as a String of length 5, it has to be unique , and it can be null
    text = db.Column(db.String(5), unique=True, nullable=False)
    xCoord = db.Column(db.Integer, nullable=False)
    yCoord = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"Point('{self.id}','{self.text}','{self.xCoord}',{self.yCoord}')"
