import csv

with open('movies.csv', newline='') as file_movies, open('links.csv', newline='') as file_links, open('movie_generated.csv', 'w', newline='') as w:
    movies = csv.DictReader(file_movies)
    links = csv.DictReader(file_links)

    writer = csv.DictWriter(w, ['movieId', 'imdbId', 'title', 'genres'])
    writer.writeheader()

    for movie, link in zip(movies, links):
        movie['imdbId'] = link['imdbId']
        writer.writerow(movie)

