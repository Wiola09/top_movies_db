"""
https://stackoverflow.com/questions/14789668/separate-sqlalchemy-models-by-file-in-flask
@johnny It means that SQLAlchemy() does not have to take app as parameter in the module it is used.
In most examples you can see SQLAlchemy(app) but it requires app from other scope in this case.
Instead you can use uninitialized SQLAlchemy() and use init_app(app) method later
as described in http://stackoverflow.com/a/9695045/2040487. –
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imdb_id = db.Column(db.String(250), unique=True, nullable=True)
    title = db.Column(db.String(250), unique=True, nullable=True)
    year = db.Column(db.String(250), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    rating = db.Column(db.String(250), nullable=True)
    ranking = db.Column(db.String(250), nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), unique=True, nullable=True)


    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Books {self.title}>'

    def add_movie(self):
        new_movie = Movie(
            id=2,
            imdb_id="55",
            title="Phone Boothaa",
            year="2002",
            description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
            rating="7.3",
            ranking="10",
            review="My favourite character was the caller.",
            # img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
            img_url = "https://m.media-amazon.com/images/M/MV5BZjY5ZjQyMjMtMmEwOC00Nzc2LTllYTItMmU2MzJjNTg1NjY0XkEyXkFqcGdeQXVyNjQ1MTMzMDQ@._V1_.jpg"
        )
        db.session.add(new_movie)
        db.session.commit()
