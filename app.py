from flask import Flask, render_template, request
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load model
model = pickle.load(open('model.pkl', 'rb'))
movies = pd.DataFrame(model['movies_dict'])
cv = model['vectorizer']

# Compute similarity once
vectors = cv.transform(movies['tags']).toarray()
similarity = cosine_similarity(vectors)


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    return [movies.iloc[i[0]].title for i in movie_list]


@app.route('/')
def home():
    return render_template('index.html', movie_list=movies['title'].values)


@app.route('/recommend', methods=['POST'])
def recommend_movies():
    movie = request.form['movie']
    recommendations = recommend(movie)
    return render_template('index.html',
                           movie_list=movies['title'].values,
                           recommendations=recommendations)


if __name__ == '__main__':
    app.run(debug=True)