import datetime

from peewee import (CharField, DateTimeField, IntegerField, Model, DateField, PostgresqlDatabase)


database = PostgresqlDatabase(None)


class BaseModel(Model):

    class Meta:
        database = database


class BigIntegerField(IntegerField):
    field_type = 'BIGINT'


class Movie(BaseModel):
    budget = BigIntegerField()
    tmdb_id = IntegerField()
    imdb_id = CharField()
    original_language = CharField()
    original_title = CharField()
    popularity = IntegerField()
    poster_path = CharField()
    release_date = DateField()
    revenue = BigIntegerField()
    runtime = IntegerField()
    opensubtittle_id = CharField(null=True)
    srt_file = CharField(null=True)
    last_upload = DateTimeField(null=True)
    created = DateTimeField(default=datetime.datetime.now)


def init_db(db_name, user, password, host, port):
    database.init(database=db_name, user=user, password=password, host=host, port=port)
    database.connect()
    database.create_tables([Movie, ])
    return database
