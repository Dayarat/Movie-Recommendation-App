from dataclasses import dataclass


@dataclass
class Movie:
    def __init__(self, title: str, imdb: str, director: str, year: int, rating: int, image: str):
        """
        Parameters:
            titile: str - Title of the Movie
            imbd: str - imbd id of the Movie
            Director: str - Director of the movie
            year: int - Year the movie was released 
            rating: int - Rating of the book
            image: str - Link to the cover photo of the Movie
        """
        self.title = title
        self.imdb = imdb
        self.director = director
        self.year = year
        self.rating = rating
        self.image = image
