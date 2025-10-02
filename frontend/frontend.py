import streamlit as st
import requests

home_page = st.Page('pages/recommendations.py', title = 'Recomendações')
search_page = st.Page('pages/search.py', title = 'Buscar Filmes')
ratings_page = st.Page('pages/ratings.py', title = 'Minhas Avaliações')

if 'users' not in st.session_state:
    st.session_state.users = requests.get('http://localhost:8000/users').json()

with st.sidebar:
    selected = st.selectbox('Usuário', [user['name'] for user in st.session_state.users])

    for user in st.session_state.users:
        if selected == user['name']:
            st.session_state.user_id = user['id']
            break

    pressed = st.button('Salvar alterações')
    if pressed:
        requests.get('http://localhost:8000/salvar')

pg = st.navigation([home_page, search_page, ratings_page])
pg.run()
