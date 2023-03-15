from flask_sqlalchemy import SQLAlchemy
from time import sleep


db = SQLAlchemy()


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ranking = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String(100))
    title = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String)
    tmdb_id = db.Column(db.Integer, unique=True)
    
    def __repr__(self) -> str:
        return f'<Movie {self.title}>'
    

def create_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
    db.init_app(app)
    with app.app_context():
        db.create_all()


def add_movie_in_db(movie_details: dict):
    new_movie = Movie(
        ranking = movie_details.get('ranking'),
        img = movie_details.get('img'),
        title = movie_details.get('title'),
        rating = movie_details.get('rating'),
        review = movie_details.get('review'),
        tmdb_id = movie_details.get('tmdb_id'),
    )
    db.session.add(new_movie)
    db.session.commit()


def get_all_movies_in_db():
    movies = Movie.query.order_by(Movie.ranking).all()
    return movies


def get_movie_in_db(movie_id):
    movie = Movie.query.filter_by(id=movie_id).one()
    return movie


def delete_movie_from_db(movie_id):
    movie = get_movie_in_db(movie_id)
    db.session.delete(movie)
    db.session.commit()


def update_movie_from_db(movie_to_update, new_rating, new_review, new_ranking):
    all_movies = get_all_movies_in_db()
    movie_to_switch = None

    for movie in all_movies:
        if movie.ranking == new_ranking:
            movie_to_switch = movie
            break
    if movie_to_switch:
        movie_to_switch.ranking = movie_to_update.ranking
    
    movie_to_update.ranking = new_ranking
    movie_to_update.rating = new_rating
    if new_review != "":
        movie_to_update.review = new_review
    
    db.session.commit()

    
