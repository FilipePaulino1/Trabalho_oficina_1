import streamlit as st
import requests

home_page = st.Page('pages/recommendations.py', title = 'Recomendações')
search_page = st.Page('pages/search.py', title = 'Buscar Filmes')
ratings_page = st.Page('pages/ratings.py', title = 'Minhas Avaliações')

with st.sidebar:
    with st.form('usuarios'):
        username = st.text_input('Usuário')
        submit = st.form_submit_button('Logar')

    if submit:
        r = requests.post('http://localhost:8000/logar', { 'username' : username }).json()
        if not r['suceeded']:
            st.error('Usuário %s não existe' % username)
        else:
            st.session_state.user_id = r['userId']

    pressed = st.button('Salvar alterações')
    if pressed:
        requests.get('http://localhost:8000/salvar')

pg = st.navigation([home_page, search_page, ratings_page])
pg.run()
