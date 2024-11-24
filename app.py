import pickle
import streamlit as st
import pandas as pd
import requests

# OMDb API key
OMDB_API_KEY = 'eb94ef36'

# Load CSS file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# Function to fetch poster and IMDb ID from OMDb API
def fetch_poster_and_imdb(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data.get("Response") == "True":
        poster = data.get("Poster", "https://via.placeholder.com/500x750.png?text=No+Poster+Available")
        imdb_id = data.get("imdbID", "")
        return poster, imdb_id
    else:
        return "https://via.placeholder.com/500x750.png?text=No+Poster+Available", ""

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    recommended_links = []

    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        poster, imdb_id = fetch_poster_and_imdb(movie_title)
        recommended_movies.append(movie_title)
        recommended_posters.append(poster)
        recommended_links.append(f"https://www.youtube.com/results?search_query={movie_title.replace(' ', '+')}+trailer")

    return recommended_movies, recommended_posters, recommended_links

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommender System')

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values)

if st.button('Show Recommendation'):
    names, posters, links = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)

    for idx, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            st.markdown(
                f"""
                <a href="{links[idx]}" target="_blank">
                    <img src="{posters[idx]}" width="150" class="movie-poster">
                </a>
                <br>
                <p style="text-align: center;">{names[idx]}</p>
                """,
                unsafe_allow_html=True
            )
