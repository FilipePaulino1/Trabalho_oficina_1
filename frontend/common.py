import streamlit as st
import requests

COL_W, COL_H = (3,20)

@st.fragment
def movies_grid(movies):
    movie_rows = [[None, None, None] for _ in range(COL_H)] 
    for i, movie in enumerate(movies):
        if i >= (COL_W*COL_H):
            break
        movie_rows[i//COL_W][i%COL_W] = movie

    for c, col in enumerate(st.columns(COL_W)):
        with col:
            for l in range(COL_H):
                movie = movie_rows[l][c]

                if movie == None:
                    break

                st.image(movie['poster_url'])
                st.markdown(f"**{movie['title']}**")

                st.caption(' | '.join(movie['genres']))

                movie_key = 'movie_%s' % movie['movieId']
                st.session_state[movie_key] = movie['rating']

                st.feedback('stars', key=movie_key, on_change=on_change_star, args=(movie_key, movie))

def on_change_star(movie_key, movie):
    stars = st.session_state[movie_key]
    r = requests.get('http://localhost:8000/avaliar', { 'userId' : st.session_state.user_id, 'movieId' : movie['movieId'], 'stars' : stars })

    if r.json()['suceeded'] == False:
        st.error('Alguma coisa deu errado ao avaliar...')
    else:
        movie['rating'] = stars
