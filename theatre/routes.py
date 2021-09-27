from flask import render_template, url_for
from . import app
from .models import Movie

@app.route('/')
@app.route('/home')
def home():
    home_movies = Movie.query.order_by(Movie.popularity.asc()).all()
    return render_template('home.html', title='Home', movies=home_movies)


@app.route('/movie/<int:id>', methods=['GET'])
def movie(id):
    movie = Movie.query.get_or_404(id)
    return render_template('movie.html', title=movie.title, movie=movie)