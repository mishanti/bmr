import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine

conns = f'postgres://localhost:5432/movie_recommender'

db = create_engine(conns, encoding='latin1', echo=False)

query = """SELECT m.title, r.rating, r.user_id
FROM movies as m
join ratings as r ON r.movie_id = m.movie_id;"""

df = pd.read_sql(query, db)
R = df.pivot_table(values="rating", index="user_id", columns="title")
# Filling NaNs
imputer = KNNImputer(n_neighbors=3)

R_filled = pd.DataFrame(imputer.fit_transform(R).round(1), columns = R.columns, index = R.index)

similarities = pd.DataFrame(cosine_similarity(R_filled), columns=R.index, index=R.index)
movies = R_filled.columns

def random_recommend(user_response):
  #user_response = {'genre': 'comedy', 'film_name1': 'Interstellar (2014)', 'rating1': '5', 'film_name2': 'Blade Runner (1982)', 'rating2': '4.8', 'film_name3': "Harry Potter and the Sorcerer's Stone (a.k.a. Harry Potter and the Philosopher's Stone) (2001)", 'rating3': '0.5'}

  user_input = {user_response["film_name1"]: float(user_response["rating1"]), user_response["film_name2"]: float(user_response["rating2"]), user_response["film_name3"]: float(user_response["rating3"])}

  # Append new user to the user-item matrix
  R_new_user = R_filled.append(pd.DataFrame(user_input, index=["user_input"]))

  # Fill the NaNs for new users
  R_new_user_filled = R_new_user.fillna(2.5)

  ### Create a filter for the missing movies
  # ~is basically saying "not": turns the boolean values around
  movie_filter = ~R_new_user.isna().any().values

  # Create an updated user list
  updated_users = R_new_user.index

  R_new_user.transpose()[movie_filter].transpose()

  # Based on new user's ratings, we want to calculate a similarity to the other users
  similarities_new_user = pd.DataFrame(cosine_similarity(R_new_user.transpose()[movie_filter].transpose()),                                     index=updated_users, columns=updated_users)

  # Predict ratings for new_user
  similarities_user_input = similarities_new_user['user_input'][~(similarities_new_user.index=='user_input')]

  # Calculate rating predictions
  rating_predictions = pd.DataFrame(                        np.dot(similarities_user_input, R_filled)                         /similarities_user_input.sum(),                         index=R.columns)

  recommended_movies = rating_predictions[~movie_filter].sort_values(by=0, ascending=False).head(5).index.tolist()
  print(recommended_movies)
  return recommended_movies
