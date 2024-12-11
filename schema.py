import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import db, Movie, Genre

class MovieType(SQLAlchemyObjectType):
    class Meta:
        model = Movie

class GenreType(SQLAlchemyObjectType):
    class Meta:
        model = Genre

class CreateGenre(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    genre = graphene.Field(lambda: GenreType)

    def mutate(self, info, name):
        genre = Genre(name=name)
        db.session.add(genre)
        db.session.commit()
        return CreateGenre(genre=genre)

class UpdateGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)

    genre = graphene.Field(lambda: GenreType)

    def mutate(self, info, id, name):
        genre = Genre.query.get(id)
        if not genre:
            raise Exception('Genre not found')
        genre.name = name
        db.session.commit()
        return UpdateGenre(genre=genre)

class DeleteGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        genre = Genre.query.get(id)
        if not genre:
            raise Exception('Genre not found')
        db.session.delete(genre)
        db.session.commit()
        return DeleteGenre(success=True)

class CreateMovie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
        release_year = graphene.Int()
        genre_ids = graphene.List(graphene.Int)

    movie = graphene.Field(lambda: MovieType)

    def mutate(self, info, title, description=None, release_year=None, genre_ids=None):
        movie = Movie(
            title=title,
            description=description,
            release_year=release_year
        )
        if genre_ids:
            genres = Genre.query.filter(Genre.id.in_(genre_ids)).all()
            movie.genres.extend(genres)
        db.session.add(movie)
        db.session.commit()
        return CreateMovie(movie=movie)

class Mutation(graphene.ObjectType):
    create_genre = CreateGenre.Field()
    update_genre = UpdateGenre.Field()
    delete_genre = DeleteGenre.Field()
    create_movie = CreateMovie.Field()

class Query(graphene.ObjectType):
    movies = graphene.List(MovieType)
    genres = graphene.List(GenreType)
    movies_by_genre = graphene.List(MovieType, genre_id=graphene.Int())
    genre_by_movie = graphene.List(GenreType, movie_id=graphene.Int())

    def resolve_movies(self, info):
        return Movie.query.all()

    def resolve_genres(self, info):
        return Genre.query.all()

    def resolve_movies_by_genre(self, info, genre_id):
        genre = Genre.query.get(genre_id)
        if not genre:
            raise Exception('Genre not found')
        return genre.movies.all()

    def resolve_genre_by_movie(self, info, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            raise Exception('Movie not found')
        return movie.genres

schema = graphene.Schema(query=Query, mutation=Mutation)
