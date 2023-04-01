import os

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Email, NumberRange
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
# from flask_sqlalchemy.exc import DBAPIError
from psycopg2.extensions import TransactionRollbackError

from api_filmovi import TMDB_API
from baza_podataka import db, Movie2, UserData, User_movie

APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "default_value")

app = Flask(__name__)
app.config['SECRET_KEY'] = APP_SECRET_KEY
Bootstrap(app)

##CREATE DATABASE

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-movies-collection.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL1", "sqlite:///neww-movies-collection3.db")
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app) # Ovaj deo je bio dok je class Nalozi(db.Model): bila definisna u ovom fajlu

db.init_app(app)  # vidi komentar u baza_podataka

""" The login manager contains the code that lets your application and Flask-Login work together, such as how to load a 
user from an ID, where to send users when they need to log in, and the like.
Once the actual application object has been created, you can configure it for login with:"""
login_manager = LoginManager()
login_manager.init_app(app)

# bez app_context() javlja gresku, mozda je do verzija Flask-SQLAlchemy==3.0.2
with app.app_context():

    db.create_all()
    # film = Movie()
    # film.add_movie()



class RateMovieForm(FlaskForm):
    # Primer koda sa svojom porukom o gresci
    # rating = IntegerField(label='Your Rating Out of 10 e.g. 8', default=7, validators=[NumberRange(min=0, max=10, message="Morate uneti pozitivan broj")])

    rating = IntegerField(label='Your Rating Out of 10 e.g. 8', default=7, validators=[NumberRange(min=0, max=10)])
    review = StringField(label='Your Review', default="Good movie", validators=[Length(min=8, max=250)])
    submit = SubmitField(label="Done")


class AddMovie(FlaskForm):
    # iako je ovde dodat, ali ne koristim validator
    title = StringField(label='Movie Title', default="Enter Movie Title", validators=[Length(min=8)])
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


""" The below code allows the app and login manager to work together. User_id allows to display unique data for 
each user at a website (like account info, past purchases, carts, etc.)"""
@login_manager.user_loader
def load_user(user_id):
    return User_movie.query.get(int(user_id))


@app.route("/add", methods=["GET", "POST"])
@login_required
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
            new_movie = Movie2(
                imdb_id=item["id"],
                title=item["title"],
                year=item['release_date'],
                description=item['overview'],
                rating=item['popularity'],
                ranking=index + 1,
                review=" ",
                img_url=f"https://image.tmdb.org/t/p/w500{item['poster_path']}",
                imdb_url=f"",
                email=current_user.email

            )
            lista.append(new_movie)
        if len(lista) == 0:
            flash("There are no results in the database for the entered value, repeat the search with a new value !")
        # print(len(lista))
        #
        # print(results)
        # print(film)
        return render_template("index.html", filmovi=lista, prikazi_dugme=da_je_stranica_sa_rezultatima_pretrage, logged_in=current_user.is_authenticated)
        return render_template("select.html", filmovi=lista)

    addmovie_form = AddMovie()
    return render_template("add.html", form=addmovie_form)

@app.route("/delete", methods=["GET", "POST"])
@login_required
def obrisi_film():
    movie_id = request.args.get('rb')
    movie_to_delete = Movie2.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    # Umesto return redirect(url_for('home_prikaz_filmova')), sa url_for biramo funkciju

    return redirect('/home_prikaz_filmova')

@app.route("/dodaj_u_bazu")
@login_required
def dodaj_u_bazu():
    film_id = request.args.get('film_id_za_dodati')
    film_rating = request.args.get('film_rating')
    print(len(film_rating))
    film_review = request.args.get('film_review')
    print(len(film_review))
    tmdb = TMDB_API()
    film = tmdb.uzmi_film_API(film_id)
    print(len(film["original_title"]), len(film["release_date"]), len(film["overview"]), len(f"https://image.tmdb.org/t/p/w500{film['poster_path']}"), len(f"https://www.imdb.com/title/{film['imdb_id']}/"))
    opis = film["overview"]
    if len(opis) > 249:
        opis2 =film["overview"][:249]
    else:
        opis2 = opis
    print(type(Movie2.imdb_id))
    print(Movie2.imdb_id)
    print(type(film["id"]))
    """ Ako vam linija koda 
    Movie2.query.filter(Movie2.email == current_user.email, Movie2.imdb_id == film["id"]).order_by(Movie2.rating).all()
     pravi problem kada nema rezultata pretrage, možete dodati provjeru da li postoji bilo koji red u odgovoru pozivom
      metode first() umjesto all(). Na taj način, ako nema odgovarajućih redova, varijabla će biti None."""

    try:
        dal_postoji_u_bazi_korisnika = Movie2.query.filter(Movie2.email == current_user.email, Movie2.imdb_id == film["id"]).order_by(Movie2.rating).first()
    except:
        db.session.rollback()
        db.session.commit()
        dal_postoji_u_bazi_korisnika = None

          # dal_postoji_u_bazi_korisnika = ""
        # print(len(dal_postoji_u_bazi_korisnika))
    if dal_postoji_u_bazi_korisnika:
        print(dal_postoji_u_bazi_korisnika, "vec postoji u bazi")
        return redirect(url_for("home_prikaz_filmova", logged_in=current_user.is_authenticated))

    new_movie = Movie2(
        imdb_id=film["id"],
        title=film["original_title"],
        year=film["release_date"],
        description=opis2,
        rating=film_rating,
        ranking="10",
        review=film_review,
        img_url=f"https://image.tmdb.org/t/p/w500{film['poster_path']}",
        imdb_url=f"https://www.imdb.com/title/{film['imdb_id']}/",
        email=current_user.email
    )
    db.session.add(new_movie)
    db.session.commit()

    return redirect(url_for("home_prikaz_filmova", logged_in=current_user.is_authenticated))
    # Morao gornju liniju zbog prenosenja info o logovanju
    return redirect("/", logged_in=current_user.is_authenticated)


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    # Argumen se daje uz pozivanje funkcije u idex.html href="{{ url_for('edit', naslov=film.id) }}"
    movie_id = request.args.get('naslov')
    film_test = request.args.get("film_id_za_dodati")

    # if petlja zaduzena za proveru da li film vec postoji u bazi, ako postoji uzima njegov id dodeljuje movie_id,
    # i dalje se nastavlja sa editovanje rewiev i rating kao da je pritisnuto dugme update
    if film_test:
        dal_postoji_u_bazi_korisnika = Movie2.query.filter(Movie2.email == current_user.email,
                                                           Movie2.imdb_id == film_test).order_by(Movie2.rating).all()
        if len(dal_postoji_u_bazi_korisnika) > 0:
            # iz nekog razloga mi generise dve poruke, pa sam u index.html morao da biram prvu poruku iz liste
            flash(f"The movie {dal_postoji_u_bazi_korisnika[0].title} already exists in the database!")
            movie_id = dal_postoji_u_bazi_korisnika[0].id
            # return redirect(url_for("home_prikaz_filmova", logged_in=current_user.is_authenticated))

    movie_to_update = Movie2.query.filter_by(id=movie_id).first()

    edit_review_and_rating_form = RateMovieForm()
    # ovde mislim da moze i if edit_review_and_rating_form.validate_on_submit():,
    # mozda samo treba pre definisati formu edit_review_and_rating_form = RateMovieForm())
    if request.method == "POST":
        # Ovde validacije forme radi svoj posao
        if edit_review_and_rating_form.validate():
            film_rating_forma = edit_review_and_rating_form.rating.data
            film_review_forma = edit_review_and_rating_form.review.data

            # # Može i ovako :
            # film_review_forma = request.form["review"]
            # film_rating_forma = request.form["rating"]
            try:
                # Prvo probava pretragu baze, ovo hvata posle pritiska "update" dugmeta, editovanje psotojeceg filma
                movie_to_update.review = film_review_forma
                movie_to_update.rating = film_rating_forma
                db.session.commit()
                return redirect(url_for('home_prikaz_filmova'))
            # Posto kada je nepostojeci film u nasoj DB javlja AttributeError to sam iskoristio
            # (mada nisam morao da specificiram gresku) i preusmerio nafunkciju za dodavanje
            # filma gde sam poslao potrebne argumente
            except AttributeError:
                return redirect(url_for("dodaj_u_bazu",
                                        film_id_za_dodati=film_test,
                                        film_rating=film_rating_forma,
                                        film_review=film_review_forma
                                        ))

        else:
            errors = edit_review_and_rating_form.errors
            print(errors)
            # prikaži greške nekako na stranici
            return render_template("edit.html", form=edit_review_and_rating_form, id=movie_to_update)

    # ovaj id mi sluzi da prenesem objekat filma <h1 class="heading">{{ id.title }}</h1>
    return render_template("edit.html", form=edit_review_and_rating_form, id=movie_to_update)



@app.route("/home_prikaz_filmova")
@login_required
def home_prikaz_filmova():
    try:
        Movie2.add_movie()
    except:
        print("vec dodat")

        # Deo koda zaduzen za sortiranje filmova od manjeg ka vecem, pa se onda obrne,
    svi_filmovi_po_logovanom_koriniku = Movie2.query.filter(Movie2.email == current_user.email).order_by(Movie2.rating).all()

    svi_filmovi_po_logovanom_koriniku.reverse()
    for i in range(len(svi_filmovi_po_logovanom_koriniku)):
        # This line gives each movie a new ranking reversed from their order in all_movies
        svi_filmovi_po_logovanom_koriniku[i].ranking = i + 1
    # print(all_books)
    dodaj_novi = False
    db.session.commit()
    print(current_user.name)
    return render_template(
        "index.html",
        filmovi=svi_filmovi_po_logovanom_koriniku,
        logged_in=current_user.is_authenticated,
        name=current_user.name
        )

@app.route('/')
def pocetak():
    return render_template("pocetak.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        user_object = UserData.pretrazi_db_po_korisniku(UserData, vrednost_za_pretragu=email)

        if user_object:
            # metod flash je iz flaska, dodat kod i u *.html stranici
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        UserData(
            name=name,
            email=email,
            password=password,
        ).add_user()
        user = User_movie.query.filter_by(email=email).first()
        """ Kada korisnik pošalje podatke za prijavu (npr. korisničko ime i lozinku), obično se ti podaci proveravaju u 
        bazi podataka kako bi se utvrdilo da li su validni. Ako su podaci validni, korisnik se "autentikuje" 
        (authenticate), što znači da se postavlja current_user objekat na instancu User klase koja predstavlja 
        prijavljenog korisnika.U Flasku se ovo obično radi pomoću login_user() funkcije, koja prima User objekat kao 
        argument i postavlja current_user na taj objekat."""
        login_user(user)

        return redirect(url_for("home_prikaz_filmova", name=name, logged_in=current_user.is_authenticated))

    return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user_object = UserData.pretrazi_db_po_korisniku(UserData, vrednost_za_pretragu=email)

        if not user_object:
            # metod flash je iz flaska, dodat kod i u *.html stranici
            flash("That email does not exist, please register.")
            return redirect(url_for('register'))

        # Password incorrect
        # Check stored password hash against entered password hashed.
        elif not check_password_hash(user_object.password, password):
            # metod flash je iz flaska, dodat kod i u *.html stranici
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))

        # Email exists and password correct
        else:  # If the user has successfully logged in or registered, you need to use the login_user() function to
               # authenticate them.
            login_user(user_object)
            return redirect(url_for('home_prikaz_filmova', name=user_object.name))

    return render_template("login.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('pocetak', logged_in=current_user.is_authenticated))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
