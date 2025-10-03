import streamlit as st
import requests
#import panda

from common import movies_grid

st.title('Recomendações')

with st.form('forma'):
    col1, col2 = st.columns(2)
    with col1:
        vizinhos = st.number_input('vizinhos', min_value=0, value=5)
    with col2:
        max_result = st.number_input('max resultado', min_value=0, value=10)

    submit = st.form_submit_button('Gerar recomendações')

if submit:
    r = requests.get('http://localhost:8000/recomendacoes/' + str(st.session_state.user_id), {'k' : vizinhos, 'n' : max_result }).json()

    if 'error' in r:
        st.error(movies['error'])

    movies = r['movies']

    vizinhos = r['vizinhos']

    common_keys = list(max([vizinho['rating'].keys() for vizinho in vizinhos])) #Converter para list para ficar ordenado

    data = {}
    data['nome'] = [vizinho['name'] for vizinho in vizinhos]

    for key in common_keys:
        data[key] = []
        for vizinho in vizinhos:
            ratings = vizinho['rating']
            data[key] += [ratings[key]+1 if key in ratings else None]

    data['sim'] = []
    for vizinho in vizinhos:
        data['sim'] += [vizinho['sim']]

    st.dataframe(data)

    movies_grid(movies)
