import os

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email

from api_filmovi import TMDB_API
from baza_podataka import db, Movie

APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "default_value")

app = Flask(__name__)
app.config['SECRET_KEY'] = APP_SECRET_KEY
Bootstrap(app)

##CREATE DATABASE

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-movies-collection2.db'
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app) # Ovaj deo je bio dok je class Nalozi(db.Model): bila definisna u ovom fajlu

db.init_app(app)  # vidi komentar u baza_podataka
##CREATE TABLE

# bez app_context() javlja gresku, mozda je do verzija Flask-SQLAlchemy==3.0.2
with app.app_context():

    db.create_all()
    # film = Movie()
    # film.add_movie()



class RateMovieForm(FlaskForm):
    rating = StringField(label='Your Rating Out of 10 e.g. 7.5', validators=[Length(min=8)])
    review = StringField(label='Your Review', validators=[Length(min=8)])
    submit = SubmitField(label="Done")


class AddMovie(FlaskForm):
    title = StringField(label='Movie Title', validators=[Length(min=8)])
    submit = SubmitField(label="Add Movie")


recnik = {'adult': False,
          'backdrop_path': None,
          'genre_ids': [99, 35],
          'id': 830700,
          'original_language': 'en',
          'original_title': 'Phone',
          'overview': 'A primer on proper phone manners produced for the New Zealand Post Office.',
          'popularity': 0.632,
          'poster_path': '/hgD2pJQLJ2PFzMOGRU5ZgDaLTjA.jpg',
          'release_date': '1974-07-07',
          'title': 'Phone',
          'video': False,
          'vote_average': 0.0,
          'vote_count': 0}


@app.route("/add", methods=["GET", "POST"])
def pretrazi_i_prikazi_filmove():

    """
    Argument se daje uz pozivanje funkcije u idex.html href="{{ url_for('add', kliknuta_pretraga=True)}}
    # na taj nacin omogucavam prikaz razlicitih dugmića na pozadini kartice jer pritiskanjem dugmeta ide se na
    # funkciju add, funkcija add otvara add.html, i formu na njoj, kada se na formi pritisne dugme vraca se
    u funkciju add vrednost polja u kom je termin pretrage za filmove, taj termin se salje u API ,
    rezultat se vraca kao json, preabcujem ga u listu i Movie objekte i saljem na pocetnu stranicu,
    ali sada saljem i vrednost "
    :return:
    """
    da_je_stranica_sa_rezultatima_pretrage = request.args.get('kliknuta_pretraga')
    print(da_je_stranica_sa_rezultatima_pretrage, "ovo")
    print(type(bool(da_je_stranica_sa_rezultatima_pretrage)))
    if request.method == "POST":
        film = request.form["title"]
        tmdb = TMDB_API()
        results = tmdb.uzmi_API(film)
        lista = []
        for index, item in enumerate(results):
            new_movie = Movie(
                imdb_id=item["id"],
                title=item["title"],
                year=item['release_date'],
                description=item['overview'],
                rating="7.3",
                ranking=index + 1,
                review=" ",
                img_url=f"https://image.tmdb.org/t/p/w500{item['poster_path']}"

            )
            lista.append(new_movie)
        # print(len(lista))
        #
        # print(results)
        # print(film)
        return render_template("index.html", filmovi=lista, prikazi_dugme=da_je_stranica_sa_rezultatima_pretrage)
        return render_template("select.html", filmovi=lista)

    addmovie_form = AddMovie()
    return render_template("add.html", form=addmovie_form)

@app.route("/dodaj_u_bazu")
def dodaj_u_bazu():
    film_id = request.args.get('rbb')
    tmdb = TMDB_API()
    film = tmdb.uzmi_film_API(film_id)
    new_movie = Movie(
        imdb_id=film["id"],
        title=film["original_title"],
        year=film["release_date"],
        description=film["overview"],
        rating="7.3",
        ranking="10",
        review="My favourite character was the caller.",
        img_url=f"https://image.tmdb.org/t/p/w500{film['poster_path']}"
    )
    db.session.add(new_movie)
    db.session.commit()
    print(film)
    print(film["original_title"])
    # print(film_id)
    # print(type(film_id))
    # print("samo test")
    return redirect("/")

@app.route("/")
def home():
    tmdb = TMDB_API()
    results = tmdb.uzmi_API("Kosovo")

    try:
        Movie.add_movie()
    except:
        print("vec dodat")

    all_books = Movie.query.order_by(Movie.rating).all()
    # print(all_books)
    dodaj_novi = False

    return render_template("index.html", filmovi=all_books)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
