import datetime

from peewee import (CharField, DateTimeField, IntegerField, Model, DateField, PostgresqlDatabase)


database = PostgresqlDatabase(None)


class BaseModel(Model):

    class Meta:
        database = database


class BigIntegerField(IntegerField):
    field_type = 'BIGINT'


class Movie(BaseModel):
    budget = BigIntegerField(null=True)
    tmdb_id = IntegerField()
    imdb_id = CharField()
    original_language = CharField()
    original_title = CharField()
    popularity = IntegerField(null=True)
    poster_path = CharField(null=True)
    release_date = DateField(null=True)
    revenue = BigIntegerField(null=True)
    runtime = IntegerField(null=True)
    subtitle_id = CharField(null=True)
    last_tweet = DateTimeField(null=True)
    created = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f'<Movie id={self.id} name={self.original_title}>'


def init_db(db_name, user, password, host, port):
    database.init(database=db_name, user=user, password=password, host=host, port=port)
    database.connect()
    database.create_tables([Movie, ])
    return database
