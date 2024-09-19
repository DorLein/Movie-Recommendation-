from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3

app = Flask(__name__)

app.secret_key = 'your_secret_key'

DATABASE = 'User.db'

def execute_query(query, params=()):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()
    connection.close()

def load_movie_data():
    movies_data = pd.read_csv('./data/movies.csv')
    return movies_data

def preprocess_data(movies_data):
    selected_features = ['genres','keywords','tagline','cast','director']
    for feature in selected_features : 
        movies_data[feature] = movies_data[feature].fillna('')
    return movies_data

def calculate_similarity(movies_data):
    combined_features = movies_data['genres']+ ' '+ movies_data['keywords']+' '+ movies_data['tagline']+' '+ movies_data['cast']+' '+ movies_data['director']
    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)
    similarity = cosine_similarity(feature_vectors)
    return similarity

def get_recommendations(movie_name, movies_data, similarity):
    list_of_all_titles = movies_data['title'].tolist()
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
    if find_close_match:
        close_match = find_close_match[0]
        index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
        similarity_score = list(enumerate(similarity[index_of_the_movie]))
        sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)[:10]
        recommended_movies = []
        for movie in sorted_similar_movies:
            index = movie[0]
            title_from_index = movies_data[movies_data.index == index]['title'].values[0]
            genre_from_index = movies_data[movies_data.index == index]['genres'].values[0]
            overview_from_index = movies_data[movies_data.index == index]['overview'].values[0]
            recommended_movies.append((title_from_index, genre_from_index, overview_from_index))
        return recommended_movies
    else:
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/newsletter')
def subsribe_newsletter():
    return render_template('newsletter.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if username or email already exists
        query = "SELECT * FROM users WHERE username = ? OR email = ?"
        params = (username, email)
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        cursor.execute(query, params)
        existing_user = cursor.fetchone()
        connection.close()

        if existing_user:
            flash('Username or email already exists. Please choose another.')
            return redirect(url_for('signup'))

        # Insert new user into the database
        query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)"
        params = (username, email, password)
        execute_query(query, params)

        flash('User successfully registered')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Retrieve user from database
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        params = (username, password)
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        cursor.execute(query, params)
        user = cursor.fetchone()
        connection.close()

        if user:
            flash('Logged in successfully')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your username and password.')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    movie_name = request.form['movie_name']
    movies_data = load_movie_data()
    movies_data = preprocess_data(movies_data)
    similarity = calculate_similarity(movies_data)
    recommendations = get_recommendations(movie_name, movies_data, similarity)

    return render_template('results_test.html', movie_name=movie_name,recommendations=recommendations)
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    
    # Check if email already exists
    query = "SELECT * FROM newsletter WHERE email = ?"
    params = (email,)
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(query, params)
    existing_email = cursor.fetchone()
    connection.close()
    
    if existing_email:
        flash('Email already subscribed.')
        return redirect(url_for('subscribe_newsletter'))
    
    # Insert new email into the newsletter table
    query = "INSERT INTO newsletter (email) VALUES (?)"
    params = (email,)
    execute_query(query, params)
    
    flash('Successfully subscribed to the newsletter.')
    return redirect(url_for('index'))
# Error handling route for 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
