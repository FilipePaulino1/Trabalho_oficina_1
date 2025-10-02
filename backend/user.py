import csv

class User():
    def __init__(self, id, name, ratings):
        self.id = id
        self.name = name
        self.ratings = ratings

users = {}

with open('dataset/users.csv', newline='') as user_file, open('dataset/ratings.csv', newline='') as ratings_file:
    csv_users = csv.DictReader(user_file)
    csv_ratings = csv.DictReader(ratings_file)

    ratings = {}
    for row in csv_ratings:
        userId = int(row['userId'])
        if userId not in ratings: ratings[userId] = []

        rating = float(row['rating'])
        ratings[userId] += [(int(row['movieId']), 0 if rating == 0.5 else int(rating)-1)]

    for row in csv_users:
        id = int(row['userId'])
        user_ratings = { movieId : rating for movieId, rating in ratings[id] } if id in ratings else {}
        users[id] = User(id, row['name'], user_ratings)
