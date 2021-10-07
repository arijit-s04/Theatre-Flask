
from sqlalchemy.orm import defaultload
from theatre import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    path = db.Column(db.String(200), nullable=False)
    poster_path = db.Column(db.String(200), nullable=False, default='default-poster.webp')
    year = db.Column(db.Integer, nullable=True)
    popularity = db.Column(db.Integer, nullable=False, default=0)
    category = db.Column(db.String(20), nullable=False, default='movie')
    description = db.Column(db.Text, nullable=True)
    number_of_ep = db.Column(db.Integer, nullable=True)

    def __repr__(self) -> str:
        return f"Movie({self.id}, {self.title}, {self.path}, {self.year}, {self.category})"
