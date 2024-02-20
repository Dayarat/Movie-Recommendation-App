import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from typing import Tuple

def read_dataset() -> pd.DataFrame:
    """
    Read the dataset from Movies.csv file.
    Return a DataFrame containing movie data.
    """
    movies = pd.read_csv("rec_sys/dataset/Movies.csv", low_memory=False)
    return movies

def save_data(rating_matrix, similarity_scores, movies):
    """
    Saves rating matrix, Movies, Movie names, and similarity scores in pickle format.
    Parameters:
        rating_matrix: pandas.DataFrame - User rating for each book
        similarity_scores: 
        movies: pandas.DataFrame - Details of the movies
    """
    pickle.dump(list(rating_matrix.index), open("rec_sys/rec_data/movie_names.pkl", "wb"))
    pickle.dump(rating_matrix, open("rec_sys/rec_data/rating_matrix.pkl", "wb"))
    pickle.dump(similarity_scores, open("rec_sys/rec_data/similarity_scores.pkl", "wb"))
    pickle.dump(movies, open("rec_sys/rec_data/movies.pkl", "wb"))


def rec_init():
    """
    Computes the similarity scores based on collaborative filtering.
    Only movies with a minimum number of ratings are considered.
    Similarity is measured based on cosine-similarity.
    """
    movies = read_dataset()

    # Filter out movies with insufficient ratings
    min_ratings = 3
    movies_with_enough_ratings = movies[movies['Rating'] >= min_ratings]

    # Create a rating matrix
    rating_matrix = movies_with_enough_ratings.pivot_table(index='Title', values='Rating', columns='IMDB ID')
    rating_matrix.fillna(0, inplace=True)

    # Compute similarity scores
    similarity_scores = cosine_similarity(rating_matrix)

    # Save data
    save_data(rating_matrix, similarity_scores, movies)

if __name__ == "__main__":
    rec_init()