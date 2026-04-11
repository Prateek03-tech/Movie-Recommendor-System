import streamlit as st
import pickle
import numpy as np
import pandas as pd
import requests ## for hitting API's

movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)  ##Giving error not able to move dataframe from pickle so
## we will change it to dictionary
similarity = pickle.load(open("similarity.pkl", "rb"))

## recommender function
def Recommend_main(movie):
    movie_index = movies[movies['title'] == movie].index[0]## for fetching index
    distances = similarity[movie_index]##array of distances from other movies
    movies_list=sorted(list(enumerate(distances)),reverse=True,key =lambda x:x[1])[1:6]##first five similar movies
    ##now we will print values of list of tuples that we will get
    recommended_movies = []
    for i in movies_list:
        movieid = movies.iloc[i[0]].movie_id## using this movie id's for fetching posters.TMDB site is blocked in India.
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

st.title("Movie Recommender System")


selected_movie = st.selectbox(
   "What to Watch?",
   movies['title'].values
)

if st.button("Recommend"):
    recommended_movies = Recommend_main(selected_movie)
    for i in recommended_movies:
        st.write(i)
