import streamlit as st
import pickle
import pandas as pd
import requests



movie_dict = pickle.load(open('movie_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movies = pd.DataFrame(movie_dict)


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    names = []
    posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwOGY5MjM2YzFiODM2Yjc0NTMyNjFkMDQyY2E3M2EzOSIsInN1YiI6IjY1ZjY4Y2RlYWUzODQzMDE3ZDQ5YzgyZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.J05KCMg1cayvouXMUXiKNC76sTvO93BZvnPLuJDKnuQ"
        }
        response = requests.get("https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id), headers=headers)
        data = response.json()
        poster = 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

        names.append(movies.iloc[i[0]].title)
        posters.append(poster)
    return names,posters


st.title("Movie reccomender system")

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values)
if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)
    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
