import json

JSON_FILE = "movies_database.json"

def read_movie_from_json_file(file_path: str, movie_id: int):
    ''' 
    Read a movie from a JSON file using the movie id
    Parameters:
    - file_path: str : path to the JSON file
    - movie_id: int : id of the movie to be read
    Returns:
    - dict : movie data if found
    '''
    try:
        with open(file_path, 'r') as file:
            movies = json.load(file)
            for movie in movies:
                if movie['id'] == movie_id:
                    return movie
            raise ValueError("Movie not found")
    except FileNotFoundError:
        raise FileNotFoundError("File not found")
    
def read_all_movies_from_json_file(file_path: str):
    '''
    Read all movies from a JSON file
    Parameters:
    - file_path: str : path to the JSON file
    Returns:
    - list : list of all movies if file found
    '''
    try:
        with open(file_path, 'r') as file:
            movies = json.load(file)
            return movies
    except FileNotFoundError:
        raise FileNotFoundError("File not found")

def write_movie_to_json_file(file_path: str, movie: dict):
    '''
    Create a movie data in a JSON file
    If same movie id exists, update the existing movie data
    with the new one, thereby avoiding duplicates
    Parameters:
    - file_path: str : path to the JSON file
    - movie: dict : movie data to be written
    Returns:
    - dict : movie data if written successfully 
    '''
    try:
        with open(file_path, 'r+') as file:
            movies = json.load(file)
            for i, m in enumerate(movies):
                if m['id'] == movie['id']:
                    movies[i] = movie
                    file.seek(0)
                    json.dump(movies, file, indent=4)
                    file.truncate()
                    return movie
            movies.append(movie)
            file.seek(0)
            json.dump(movies, file, indent=4)
            return movie
    except FileNotFoundError:
        raise FileNotFoundError("File not found")
    
def update_movie_in_json_file(file_path: str, movie_id: int, movie: dict):
    '''
    Update a movie data in a JSON file using the movie id
    Parameters:
    - file_path: str : path to the JSON file
    - movie_id: int : id of the movie to be updated
    - movie: dict : updated movie data
    Returns:
    - dict : updated movie data if found and updated
    '''
    try:
        with open(file_path, 'r+') as file:
            movies = json.load(file)
            for i, m in enumerate(movies):
                if m['id'] == movie_id:
                    movies[i] = movie
                    file.seek(0)
                    json.dump(movies, file, indent=4)
                    file.truncate()
                    return movie
            raise ValueError("Movie not found")
    except FileNotFoundError:
        raise FileNotFoundError("File not found")

def delete_movie_from_json_file(file_path: str, movie_id: int):
    '''
    Delete a movie data from a JSON file using the movie id
    Parameters:
    - file_path: str : path to the JSON file
    - movie_id: int : id of the movie to be deleted
    Returns:
    - dict : deleted movie data if found and deleted
    '''
    try:
        with open(file_path, 'r+') as file:
            movies = json.load(file)
            for i, m in enumerate(movies):
                if m['id'] == movie_id:
                    deleted_movie = movies.pop(i)
                    file.seek(0)
                    json.dump(movies, file, indent=4)
                    file.truncate()
                    return deleted_movie
            raise ValueError("Movie not found")
    except FileNotFoundError:
        raise FileNotFoundError("File not found")

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Nithin-flix"}

@app.get("/movies")
def get_movies():
    ''' Read all movies '''
    return read_all_movies_from_json_file(JSON_FILE)

@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    ''' Read a movie by id '''
    return read_movie_from_json_file(JSON_FILE, movie_id)

@app.post("/movies")
def create_movie(movie: dict):
    ''' Create a movie '''
    return write_movie_to_json_file(JSON_FILE, movie)

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie: dict):
    ''' Update a movie by id '''
    return update_movie_in_json_file(JSON_FILE, movie_id, movie)

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    ''' Delete a movie by id '''
    return delete_movie_from_json_file(JSON_FILE, movie_id)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
