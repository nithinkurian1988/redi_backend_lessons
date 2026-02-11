# **My Movie App**

A simple FAST-API based backend application which will displays the movie details on a web page.

## **Overview**

This project provides a RESTful API to manage movie records. It includes endpoints to add, read, update, and delete movies, with data stored in an in-memory list for simplicity. The application also serves a static HTML page that displays the list of movies in a visually appealing format. The movie data is fetched from the local database or from the OMDb API, and the application uses Jinja2 templates to render the HTML page.

## **Installation**

```bash
# Navigate to the project directory
cd lesson_6
# Create a virtual environment
python -m venv venv
# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```
## **Start the Server**

```bash
uvicorn movies_app:app --reload
```

## **Access Documentation**

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## **Endpoints**

#### **GET `/movies`**
Returns a list of all movies in the database.

#### **GET `/movies/{movie_name}`**
Returns a specific movie by its name from the database or from the OMDb API if not found in the database.

#### **POST `/movies`**
Adds a new movie to the database. The request body should contain the movie details in JSON format.

#### **PUT `/movies`**
Updates an existing movie in the database. The request body should contain the updated movie details in JSON format.

#### **DELETE `/movies/{movie_name}`**
Deletes a specific movie from the database.