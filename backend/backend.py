#Backend para sistema de recomendação
from fastapi import FastAPI, Response, Form
from typing import Annotated

import requests
import math
import csv

from user import users
from movie import movies, movie_genres

def cosine_similarity(u_ratings: dict, v_ratings: dict) -> float:
    comuns = set(u_ratings.keys()) & set(v_ratings.keys())
    if not comuns:
        return 0.0

    dot = sum(u_ratings[m] * v_ratings[m] for m in comuns)
    norm_u = math.sqrt(sum(u_ratings[m] ** 2 for m in comuns))
    norm_v = math.sqrt(sum(v_ratings[m] ** 2 for m in comuns))

    if norm_u == 0 or norm_v == 0:
        return 0.0
    return dot / (norm_u * norm_v)

app = FastAPI()

@app.post("/logar")
async def login(username: Annotated[str, Form()]):
    for user in users.values():
        if user.name == username:
            return { 'suceeded' : True, 'userId' : user.id }

    return { 'suceeded' : False }

@app.get("/users")
async def usuarios():
    return [
        {
            "id": user.id,
            "name": user.name
        }
        for user in users.values()
    ]

@app.get("/salvar")
async def salvar():
    with open('dataset/ratings.csv', newline='') as f:
        writer = csv.DictWriter(f, ['userId', 'movieId', 'rating'])
        writer.writeheader()

        for user in users.values():
            for movieId, rating in user.ratings.items():
                writer.writerow([user.id, movieId, rating])

    return { 'success' : True }

@app.get("/avaliar")
async def avaliar(userId: int, movieId: int, stars: int | None = None):
    if stars == None:
        if movieId in users[userId].ratings:
            del users[userId].ratings[movieId]
    else:
        users[userId].ratings[movieId] = stars

    return { 'suceeded' : True }

@app.get("/search")
async def search(userId: int, q: str, n: int, genre: str | None = None):
    return [
        {
            "movieId": movie.id,
            "title": movie.title,
            "poster_url": 'https://img.omdbapi.com/?apikey=%s&i=tt%s' % (OMDBAPI_KEY, movie.imdb_id),
            "genres" : movie.genres,
            "rating" : users[userId].ratings[movie.id] if movie.id in users[userId].ratings else None
        }
        for movie in movies.values() if q.lower() in movie.title.lower() and (genre is None or set(genre.split('|')).issubset(set(movie.genres)))
    ][:n]

@app.get("/generos")
async def generos():
    return movie_genres

OMDBAPI_KEY = 'd48f284f'

@app.get("/avaliacoes/{userId}")
async def avaliacoes(userId: int):
    if userId not in users:
        return { 'error' : 'Usuário ID %s não existe' % userId }

    response = [
        {
            "movieId": movie_id,
            "title": movies[movie_id].title,
            "poster_url": 'https://img.omdbapi.com/?apikey=%s&i=tt%s' % (OMDBAPI_KEY, movies[movie_id].imdb_id),
            "genres" : movies[movie_id].genres,
            "rating" : rating
        }
        for movie_id, rating in users[userId].ratings.items()
    ]

    return sorted(response, key=lambda u: u['rating'], reverse=True)


@app.get("/recomendacoes/{userId}")
def recomendacoes(userId: int, k: int = 5, n: int = 20):
    """
    Retorna até `n` recomendações para o usuário `userId`,
    usando filtragem colaborativa User-User com similaridade cosseno.
    """
    if userId not in users:
        return {"error": "Usuário não encontrado"}

    target = users[userId]

    # Similaridade com outros usuários
    sims = []
    for other_id, other in users.items():
        if other_id == userId:
            continue
        sim = cosine_similarity(target.ratings, other.ratings)
        if sim > 0:
            sims.append((other_id, sim))

    if not sims:
        return {"error": "Não há usuários semelhantes para calcular recomendações"}

    sims.sort(key=lambda x: x[1], reverse=True)
    vizinhos = sims[:k]

    # Previsão de notas
    notas_previstas = {}
    for movie_id, movie in movies.items():
        if movie_id in target.ratings:
            continue

        numerador = 0.0
        denominador = 0.0
        for other_id, sim in vizinhos:
            other = users[other_id]
            if movie_id in other.ratings:
                numerador += sim * other.ratings[movie_id]
                denominador += sim

        if denominador > 0:
            notas_previstas[movie_id] = numerador / denominador

    recomendacoes = sorted(notas_previstas.items(), key=lambda x: x[1], reverse=True)[:n]
    resposta = {}

    resposta['movies'] = [
        {
            "movieId": movie_id,
            "title": movies[movie_id].title,
            "poster_url": 'https://img.omdbapi.com/?apikey=%s&i=tt%s' % (OMDBAPI_KEY, movies[movie_id].imdb_id),
            "genres" : movies[movie_id].genres,
            "rating": movies[movie_id].get_ratings(), #Média das avaliações
            #"predicted_rating": round(predicted_rating, 2)
        }
        for movie_id, predicted_rating in recomendacoes
    ]

    vizinhos = [(userId, 1)] + vizinhos

    resposta['vizinhos'] = [
        {
            "name": users[userId].name,
            "rating": { movies[k].title : v for k, v in users[userId].ratings.items() },
            "sim": s
        }
        for userId, s in vizinhos
    ]

    return resposta
