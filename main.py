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

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-movies-collection4.db'
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
    submit = SubmitField(label="Search By Name")


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
    # ovde mislim da moze i if form.validate_on_submit():, mozda samo treba pre definisati formu addmovie_form = AddMovie()
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
                rating=item['popularity'],
                ranking=index + 1,
                review=" ",
                img_url=f"https://image.tmdb.org/t/p/w500{item['poster_path']}",
                imdb_url=f""

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

@app.route("/delete", methods=["GET", "POST"])
def obrisi_film():
    movie_id = request.args.get('rb')
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    # Umesto return redirect(url_for('home')), sa url_for biramo funkciju
    return redirect('/')

@app.route("/dodaj_u_bazu")
def dodaj_u_bazu():
    film_id = request.args.get('film_id_za_dodati')
    film_rating = request.args.get('film_rating')
    film_review = request.args.get('film_review')
    tmdb = TMDB_API()
    film = tmdb.uzmi_film_API(film_id)
    new_movie = Movie(
        imdb_id=film["id"],
        title=film["original_title"],
        year=film["release_date"],
        description=film["overview"],
        rating=film_rating,
        ranking="10",
        review=film_review,
        img_url=f"https://image.tmdb.org/t/p/w500{film['poster_path']}",
        imdb_url=f"https://www.imdb.com/title/{film['imdb_id']}/"
    )
    db.session.add(new_movie)
    db.session.commit()

    return redirect("/")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    # Argumen se daje uz pozivanje funkcije u idex.html href="{{ url_for('edit', naslov=film.id) }}"
    movie_id = request.args.get('naslov')
    print(movie_id)
    film_test = request.args.get("film_id_za_dodati")
    print(film_test)

    movie_to_update = Movie.query.filter_by(id=movie_id).first()
    print(movie_to_update)
    # ovde mislim da moze i if edit_review_and_rating_form.validate_on_submit():,
    # mozda samo treba pre definisati formu edit_review_and_rating_form = RateMovieForm())

    if request.method == "POST":
        film_review_forma = request.form["review"]
        film_rating_forma = request.form["rating"]
        try:
            # Prvo probava pretragu baze, ovo hvata posle pritiska "update" dugmeta, editovanje psotojeceg filma
            movie_to_update.review = film_review_forma
            movie_to_update.rating = film_rating_forma
            db.session.commit()
            return redirect(url_for('home'))
        # Posto kada je nepostojeci film u nasoj DB javlja AttributeError to sam iskoristio
        # (mada nisam morao da specificiram gresku) i preusmerio nafunkciju za dodavanje
        # filma gde sam poslao potrebne argumente
        except AttributeError:
            return redirect(url_for("dodaj_u_bazu",
                                    film_id_za_dodati=film_test,
                                    film_rating=film_rating_forma,
                                    film_review=film_review_forma
                                    ))
    edit_review_and_rating_form = RateMovieForm()

    # ovaj id mi sluzi da prenesem objekat filma <h1 class="heading">{{ id.title }}</h1>
    return render_template("edit.html", form=edit_review_and_rating_form, id=movie_to_update)



@app.route("/")
def home():
    try:
        Movie.add_movie()
    except:
        print("vec dodat")

    # Deo koda zaduzen za sortiranje filmova od manjeg ka vecem, pa se onda obrne,
    svi_filmovi_sortirani = Movie.query.order_by(Movie.rating).all()
    svi_filmovi_sortirani.reverse()
    for i in range(len(svi_filmovi_sortirani)):
        # This line gives each movie a new ranking reversed from their order in all_movies
        svi_filmovi_sortirani[i].ranking = i + 1
    # print(all_books)
    dodaj_novi = False
    db.session.commit()
    return render_template("index.html", filmovi=svi_filmovi_sortirani)

@app.route('/register', methods=["GET", "POST"])
def register():
    pass

@app.route('/login', methods=["GET", "POST"])
def login():
    pass

@app.route('/logout')
def logout():
    pass


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
