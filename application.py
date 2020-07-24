from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

import logging

import recommender
from recommender import random_recommend

logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)

app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY']='my_love_dont_try' # a reference to the current python script
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://localhost/movie_recommender'

#inspired by http://abdulbaqi.io/2017/11/26/flask-form-ajax-sqlalchemy/

class InputForm(FlaskForm):
  film_name1 = StringField('Film name', validators=[DataRequired(),
  Length(max=100)],render_kw={"placeholder": "Enter a film name"})

  film_name2 = StringField('Film name', validators=[DataRequired(),
  Length(max=100)],render_kw={"placeholder": "Enter a film name"})

  film_name3 = StringField('Film name', validators=[DataRequired(),
  Length(max=100)],render_kw={"placeholder": "Enter a film name"})

db = SQLAlchemy(app)

class MovieName(db.Model):
  __tablename__ = 'movies'

  movie_id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(170), unique=True, nullable = False)
  genres = db.Column(db.String(100), unique=True, nullable = False)

@app.route('/')
@app.route('/index')
def index():
  form = InputForm()
  #form2 = InputForm()
  #form3 = InputForm()
  return render_template('index.html',
  #choices=MOVIES,
    form=form)

@app.route('/hello/<name>')
def hello(name):
  return render_template('hello.html', name_html=name)

@app.route('/form')
def sdg():
  form = InputForm()
  return render_template('sdg.html', form=form)

@app.route('/movies')
def moviedic():
  list_movies = []
  res = MovieName.query.all()
  my_list = [r.title for r in res]
  for one_item in my_list:
    list_movies.append({"name":one_item})
  return jsonify(list_movies)

@app.route('/recommendation')
def recommend():
  user_response = dict(request.args)
  print(user_response)

  #movies = random_recommend(user_input)
  movies = random_recommend(user_response)
  return render_template('recommendation.html', movies=movies)



  def __repr__(self):

    return '{} - {}'.format(self.iso, self.name)

  def as_dict(self):
    return {'name': self.name}

if __name__ == '__main__':
  #if I run this file + python in terminal, please run the following code
  app.run(debug=True, use_reloader=True)
