from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True

### DATABASE ###
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

cast = db.Table('cast',
                db.Column('movie_id', db.Integer,db.ForeignKey('movies.movie_id'), primary_key=True),
                db.Column('actor_id', db.Integer, db.ForeignKey('actors.actor_id'), primary_key=True)

)

class Actors(db.Model):
    actor_id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(250), nullable=False)
    birth_day = db.Column(db.String(12), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    pic = db.Column(db.Text, nullable = False)
    castlist = db.relationship('Movies', secondary=cast, backref=db.backref('castlist', lazy="dynamic"))

    def __init__(self, name, birth_day, birth_year, pic):
        self.name = name
        self.birth_day = birth_day
        self.birth_year = birth_year
        self.pic = pic

class Movies(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    director = db.Column(db.String(250), nullable=False)
    synopsis = db.Column(db.Text, nullable = False)
    poster = db.Column(db.Text, nullable = False)

    def __init__(self, title, year, director, synopsis, poster):
        self.title = title
        self.year = year
        self.director = director
        self.synopsis = synopsis
        self.poster = poster

class Pairings(db.Model):
    r_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    love_interest1 = db.Column(db.String(250), nullable=False)
    pic1 = db.Column(db.Text, nullable = False)
    love_interest2 = db.Column(db.String(250), nullable=False)
    pic2 = db.Column(db.Text, nullable = False)
    relation = db.Column(db.Text, nullable = False)

    def __init__(self, title, year, love_interest1, pic1, love_interest2, pic2, relation):
        self.title = title
        self.year = year
        self.love_interest1 = love_interest1
        self.pic1 = pic1
        self.love_interest2 = love_interest2
        self.pic2 = pic2
        self.relation = relation

@app.route('/')
def index():
    movies = Movies.query.all()

    return render_template("index.html", movies=movies)

@app.route('/title/<id>')
def title(id):
    movie = Movies.query.filter_by(movie_id = id).first()
    # actors = Actors.query.join(cast).join(Movies).filter(cast.c.movie_id == id).all()
    pairs = Pairings.query.filter_by(title = movie.title).all()

    return render_template("title.html", movie=movie, pairs=pairs)
