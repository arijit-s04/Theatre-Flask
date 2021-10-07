from flask import render_template, url_for, redirect, request, flash, abort
from . import app, db
from .models import Movie
from .utils import (deleteShow, getVideoMetadata, isAdmin,\
    login_required, saveForm, retrieveKeyWords,\
    checkCredentialsAndLogin, saveFormSeries, logoutUser)
from .forms import AdminLoginForm, ShowAddForm, ShowUpdateForm
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


@app.route('/movie/watch/<int:id>/', methods=['GET'])
def movie(id):
    movie = Movie.query.get_or_404(id)
    metadata = getVideoMetadata(movie.path)
    return render_template('movie.html', title=movie.title, movie=movie, metadata=metadata)


@app.route('/series/<int:id>/')
def series(id):
    movie = Movie.query.get_or_404(id)
    return render_template('series_overview.html', movie=movie)


@app.route('/series/<int:id>/watch/episode_<int:ep_no>/')
def episode(id, ep_no):
    movie = Movie.query.get_or_404(id)
    if ep_no > movie.number_of_ep:
        abort(404)
    metadata = getVideoMetadata(f'{movie.path}/Ep_{ep_no}.mp4')
    return render_template('episode.html', metadata=metadata, movie=movie, episode=ep_no, episode_path=f'{movie.path}/Ep_{ep_no}.mp4')


@app.route('/admin/add_show/', methods=['GET', 'POST'])
@login_required
def add_show():
    form = ShowAddForm()
    series_files_check = None
    if form.category.data == 'series':
        files  = request.files.getlist('path')
        if any(x.mimetype.split('/')[1] != 'mp4' for x in files):
            series_files_check = True
    if form.validate_on_submit() and not series_files_check:
        movie = None
        if form.category.data == 'movie':
            movie = saveForm(form)
        else:
            files  = request.files.getlist('path')
            movie = saveFormSeries(form, files)

        if movie:
            db.session.add(movie)
            db.session.commit()
            flash("Show Added!!!", "success")
            return redirect(url_for('admin'))
        print("Something wrong occured")
    print(series_files_check)
    return render_template('add_show.html', title='Admin', form=form, admin=True, series_files_check = series_files_check)


@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    if isAdmin():
        return redirect(url_for('admin_home'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        result = checkCredentialsAndLogin(form)
        if result[0]:
            flash(result[1], 'success')
            return redirect(url_for('admin_home'))
        flash(result[1], 'warning')
    return render_template('admin.html', form=form)


@app.route('/admin/logout/')
def logout():
    if isAdmin():
        logoutUser()
    return redirect(url_for('home'))


@app.route('/admin/home/')
@login_required
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


@app.route('/admin/update_show/<int:id>/', methods=['GET', 'POST'])
@login_required
def update_show(id):
    movie = Movie.query.get_or_404(id)
    form = ShowUpdateForm()
    if form.validate_on_submit():
        need_update = False
        if form.title.data != movie.title:
            movie.title = form.title.data
            need_update = True
        if form.description.data != movie.description:
            movie.description = form.description.data
            need_update = True
        if form.year.data != movie.year:
            movie.year = form.year.data
            need_update = True
        if need_update:
            db.session.commit()
            flash("Details Updated!", "success")
        return redirect(url_for('update_show', id=movie.id))
    elif request.method == 'GET':
        form.title.data = movie.title
        form.description.data = movie.description
        form.year.data = movie.year
    return render_template('update_show.html', title="Update", form=form, admin=True, movie=movie)


@app.route('/admin/delete_show/<int:id>/', methods=['POST'])
@login_required
def delete_show(id):
    movie = Movie.query.get_or_404(id)
    if deleteShow(movie):
        db.session.delete(movie)
        db.session.commit()
        flash("Show Deleted!", "success")
    else:
        flash("Something went wrong", "info")

    return redirect(url_for('admin_home'))
