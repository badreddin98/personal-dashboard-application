# Movie Database GraphQL API

This project implements a GraphQL API for managing a movie database. It allows users to create, read, update, and delete movies and genres, as well as establish relationships between them.

## Features

- Create, update, and delete genres
- Create movies with multiple genres
- Query movies by genre
- Query genres by movie
- Full CRUD operations support

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Access the GraphQL interface at: http://localhost:5000/graphql

## Example Queries

### Create a Genre
```graphql
mutation {
  createGenre(name: "Action") {
    genre {
      id
      name
    }
  }
}
```

### Create a Movie
```graphql
mutation {
  createMovie(
    title: "The Matrix"
    description: "A computer programmer discovers a mysterious world..."
    releaseYear: 1999
    genreIds: [1]
  ) {
    movie {
      id
      title
      genres {
        name
      }
    }
  }
}
```

### Query Movies by Genre
```graphql
query {
  moviesByGenre(genreId: 1) {
    id
    title
    description
  }
}
```

## Project Structure

- `app.py`: Main application file
- `models.py`: SQLAlchemy models
- `schema.py`: GraphQL schema definitions
- `requirements.txt`: Project dependencies
