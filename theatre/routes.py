from flask import render_template, url_for, redirect, request, flash, session, abort
from . import app, db
from .models import Movie
from .utils import getVideoMetadata, saveForm, retrieveKeyWords, checkCredentials
from .forms import AdminLoginForm, ShowAddForm
from sqlalchemy import or_


@app.route('/', methods=['GET'])
@app.route('/home/', methods=['GET'])
def home():
    search_query = request.args.get('search', None, type=str)
    home_movies = None
    if search_query:
        key_list = retrieveKeyWords(search_query)
        home_movies = Movie.query.filter(or_(*key_list)).all()
    else:
        home_movies = Movie.query.order_by(Movie.popularity.asc()).all()
    return render_template('home.html', title='Home', movies=home_movies, previous_query=search_query)


@app.route('/movie/<int:id>/', methods=['GET'])
def movie(id):
    movie = Movie.query.get_or_404(id)
    metadata = getVideoMetadata(movie.path)
    return render_template('movie.html', title=movie.title, movie=movie, metadata=metadata)


@app.route('/admin/add_show/', methods=['GET', 'POST'])
def add_show():
    if not isinstance(session.get('admin', None), bool):
        abort(403)
    form = ShowAddForm()
    if form.validate_on_submit():
        movie = saveForm(form)
        if movie:
            db.session.add(movie)
            db.session.commit()
            return redirect(url_for('admin'))
        print("Something wrong occured")
        
    return render_template('add_show.html', title='Admin', form=form, admin=True)


@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    if isinstance(session.get('admin', None), bool):
        return redirect(url_for('admin_home'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        result = checkCredentials(form)
        session.permanent = False
        if result[0]:
            session['admin'] = True
            flash(result[1], 'success')
            return redirect(url_for('admin_home'))
        flash(result[1], 'warning')
    return render_template('admin.html', form=form)


@app.route('/admin/logout/')
def logout():
    if isinstance(session.get('admin', None), bool):
        session.pop('admin')
    return redirect(url_for('home'))


@app.route('/admin/home/')
def admin_home():
    search_query = request.args.get('search', None, type=str)
    home_movies = None
    if search_query:
        key_list = retrieveKeyWords(search_query)
        home_movies = Movie.query.filter(or_(*key_list)).all()
    else:
        home_movies = Movie.query.order_by(Movie.popularity.asc()).all()
    return render_template('home.html', title='Home',\
        movies=home_movies, previous_query=search_query, admin=True)

