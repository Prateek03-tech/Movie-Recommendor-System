from flask import Flask, render_template, request
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load model
model = pickle.load(open('model.pkl', 'rb'))

# Convert to DataFrame
movies = pd.DataFrame(model['movies_dict'])

# Load vectorizer
cv = model['vectorizer']

# Create vectors (only once)
vectors = cv.transform(movies['tags']).toarray()


# ✅ Optimized recommendation (NO full similarity matrix)
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]

        # Compute similarity ONLY for selected movie
        distances = cosine_similarity(
            vectors[index].reshape(1, -1),
            vectors
        ).flatten()

        # Get top 5 similar movies
        movies_list = sorted(
            list(enumerate(distances)),
            reverse=True,
            key=lambda x: x[1]
        )[1:6]

        return [movies.iloc[i[0]].title for i in movies_list]

    except:
        return []


# Home route
@app.route('/')
def home():
    return render_template(
        'index.html',
        movie_list=movies['title'].values
    )


# Recommendation route
@app.route('/recommend', methods=['POST'])
def recommend_movies():
    movie = request.form.get('movie')

    recommendations = recommend(movie)

    return render_template(
        'index.html',
        movie_list=movies['title'].values,
        recommendations=recommendations
    )


# Run app
if __name__ == "__main__":
    app.run(debug=True)