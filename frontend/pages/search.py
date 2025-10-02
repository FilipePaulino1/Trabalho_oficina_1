import streamlit as st
import requests

from common import movies_grid

st.title('Buscar filmes')

if 'genres' not in st.session_state:
    st.session_state.genres = requests.get('http://localhost:8000/generos').json()

with st.form('Busca'):
    search_word = st.text_input('Procurar')
    max_results = st.number_input('Max de resultados', value=15)
    genres = st.pills('Gêneros', st.session_state.genres, selection_mode='multi')
    submit = st.form_submit_button('Submit')

if submit:
    params = { 'userId' : st.session_state.user_id, 'q' : search_word, 'n' : max_results }
    if len(genres) > 0:
        params['genre'] = '|'.join(genres)
    r = requests.get('http://localhost:8000/search', params)
    movies_grid(r.json())
