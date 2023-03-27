"""
https://stackoverflow.com/questions/14789668/separate-sqlalchemy-models-by-file-in-flask
@johnny It means that SQLAlchemy() does not have to take app as parameter in the module it is used.
In most examples you can see SQLAlchemy(app) but it requires app from other scope in this case.
Instead you can use uninitialized SQLAlchemy() and use init_app(app) method later
as described in http://stackoverflow.com/a/9695045/2040487. –
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class Movie2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imdb_id = db.Column(db.String(250), nullable=True)
    title = db.Column(db.String(260), nullable=True)
    year = db.Column(db.String(270), nullable=True)
    description = db.Column(db.String(280), nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    ranking = db.Column(db.String(290), nullable=True)
    review = db.Column(db.String(300), nullable=True)
    img_url = db.Column(db.String(310), nullable=True)
    imdb_url = db.Column(db.String(320), nullable=True)
    email = db.Column(db.String(100), nullable=True)


    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Books {self.title}>'

    def add_movie(self):
        new_movie = Movie2(
            id=2,
            imdb_id="55",
            title="Phone Boothaa",
            year="2002",
            description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
            rating="7.3",
            ranking="10",
            review="My favourite character was the caller.",
            # img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
            img_url = "https://m.media-amazon.com/images/M/MV5BZjY5ZjQyMjMtMmEwOC00Nzc2LTllYTItMmU2MzJjNTg1NjY0XkEyXkFqcGdeQXVyNjQ1MTMzMDQ@._V1_.jpg",

        )
        db.session.add(new_movie)
        db.session.commit()


class User_movie(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class UserData:
    def __init__(self, email, password, name):
        self.email = email
        self.password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        self.name = name

    def add_user(self):
        new_user = User_movie(email=self.email, password=self.password, name=self.name)
        db.session.add(new_user)
        db.session.commit()

    def pretrazi_db_po_korisniku(self, vrednost_za_pretragu):
        return User_movie.query.filter_by(email=vrednost_za_pretragu).first()