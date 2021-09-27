
from theatre import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    path = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    popularity = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self) -> str:
        return f"Movie({self.title}, {self.path}, {self.year}, {self.popularity})"
