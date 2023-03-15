import os
from flask import Flask
from flask import render_template, redirect
from flask import url_for
from flask import request
from manage_tmdb_api import get_movie, get_details, get_popular_movies
from forms import AddForm, ReviewForm, UpdateForm
from manage_db import (
    create_db, 
    add_movie_in_db, 
    get_all_movies_in_db,
    get_movie_in_db,
    delete_movie_from_db,
    update_movie_from_db,
    )


TMDB_IMG_URL = 'https://image.tmdb.org/t/p/w500/'
POSSIBLE_RANKS = (1, 2, 3, 4, 5, 6, 7, 8, 9)
SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
create_db(app)


@app.route('/')
def index():
    all_movies_from_db = get_all_movies_in_db()
    global POSSIBLE_RANKS
    all_movies_sorted = []  
    for rank in POSSIBLE_RANKS:
        item = next((movie for movie in all_movies_from_db if movie.ranking == rank), None)
        all_movies_sorted.append(item)
    return render_template('index.html', all_movies=all_movies_sorted, possible_rankings=POSSIBLE_RANKS)


@app.route('/search/<ranking>', methods=['POST', 'GET'])
def search(ranking):
    add_form = AddForm()
    result = None
    if request.method == 'POST':
        movie_name = request.form['movie']
        result = get_movie(movie_name)
    return render_template('add.html', form=add_form, movies=result, img_url=TMDB_IMG_URL, ranking=ranking)


@app.route('/search/<ranking>/popular')
def popular_movies(ranking):
    add_form = AddForm()
    result = get_popular_movies()
    return render_template('add.html', form=add_form, movies=result, img_url=TMDB_IMG_URL, ranking=ranking)


@app.route('/selected_movie/<movie_title>/<ranking>/<tmdb_id>', methods=['POST', 'GET'])
@app.route('/selected_movie/<movie_title>/<ranking>/<tmdb_id>/<poster_path>', methods=['POST', 'GET'])
def show_selected_movie(movie_title, ranking, tmdb_id, poster_path=None):
    review_form = ReviewForm()
    if review_form.validate_on_submit():
        if poster_path:
            poster_path = TMDB_IMG_URL + poster_path
        movie_details = {
            'ranking': ranking,
            'img': poster_path,
            'title': movie_title,
            'rating': review_form.rating.data,
            'review': review_form.review.data,
            'tmdb_id': tmdb_id
        }
        add_movie_in_db(movie_details)
        return redirect(url_for('index'))
    return render_template('selected.html', form=review_form, title=movie_title, poster=poster_path, img_url=TMDB_IMG_URL)


@app.route("/delete/<movie_id>")
def delete_movie(movie_id):
    delete_movie_from_db(movie_id)
    return redirect(url_for('index'))


@app.route("/update/<movie_id>", methods=['POST', 'GET'])
def update_movie(movie_id):
    update_form = UpdateForm()
    movie_to_update = get_movie_in_db(movie_id)
    if update_form.validate_on_submit():
        new_rating = update_form.rating.data
        new_review = update_form.review.data
        new_ranking = int(update_form.ranking.data)
        update_movie_from_db(movie_to_update, new_rating, new_review, new_ranking)
        return redirect(url_for('index'))
    # In the case bellow 'poster' is equal to 'img_url' + 'poster_path', so it is the full url itself
    # img_url is equal to "" because in selected.html it will concatenate with poster
    return render_template('selected.html', form=update_form, title=movie_to_update.title, poster=movie_to_update.img, img_url="")    


@app.route("/details/<int:tmdb_id>")
def get_movie_details(tmdb_id):
    movie = get_details(tmdb_id)
    background_img_path = movie.get("backdrop_path")
    if background_img_path is None:
        background = None
    else:
        background = TMDB_IMG_URL + background_img_path
    details = {
        "background_img": background,
        "homepage": movie.get("homepage"),
        "original_language": movie.get("original_language"),
        "original_title": movie.get("original_title"),
        "overview": movie.get("overview"),
        "release_date": movie.get("release_date"),
        "runtime": movie.get("runtime"),
        "tagline": movie.get("tagline"),
        "user_rating": int(round(movie.get("vote_average"), 1) * 10),
    }
    return render_template('movie_details.html', details=details)




if __name__ == '__main__':
    app.run(debug=True)