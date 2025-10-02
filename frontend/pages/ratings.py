from common import movies_grid
import streamlit as st
import requests

st.title('Minhas Avaliações')

response = requests.get('http://localhost:8000/avaliacoes/' + str(st.session_state.user_id)).json()

if 'error' in response:
    st.error(response['error'])

#print('response =', response)

movies_grid(response)
