# MovieWordCloud

A Twitter bot that tweets word clouds based on movies scripts.


# How to use

1. Clone this repo

```
$ git clone https://github.com/Bgeninatti/MovieWordCloud.git
```

2. Fill your database, TMDB and twitter credentials in the `auth.env` file:

3. Run the docker container

```
docker compose up -d
```

The command will hang forever. This means the container is running and waiting for commands.

The following commands needs to be ran in a separated shell


4. Download movies data

```
$ docker compose exec mwc mwc sync-tmdb
```

6. Download subtitles for the movies

```
$ docker compose exec mwc mwc download-missing-subtitles
```

7. Tweet a random movie

```
$ docker compose exec mwc mwc tweet-movie
```
