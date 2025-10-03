from statistics import mean
import csv

from user import users

class Movie():
    def __init__(self, id, title, imdb_id, genres):
        self.id = id
        self.title = title
        self.imdb_id = imdb_id
        self.genres = genres

    def get_ratings(self):
        rating = []
        for user in users.values():
            if self.id in user.ratings:
                rating += [user.ratings[self.id]]
        
        return int(mean(rating))

movies = {}
movie_genres = set()

with open('dataset/movies.csv', newline='') as file_movies:
    csv_movies = csv.DictReader(file_movies)

    for row in csv_movies:
        genres = row['genres'].split('|')
        movieId = int(row['movieId'])

        #Desconsidere os filmes que nenhum usuário avaliou
        rated = False
        for user in users.values():
            if movieId in user.ratings:
                rated = True
                break
        
        if not rated:
            continue

        movies[movieId] = Movie(movieId, row['title'].strip('"'), row['imdbId'], genres)

        for genre in genres:
            movie_genres.add(genre)
