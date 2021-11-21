# MovieWordCloud

A Twitter bot that tweets word clouds based on movies scripts.


# How to use

1. Clone this repo

```
$ git clone https://github.com/Bgeninatti/MovieWordCloud.git
```
2. Up the docker container

```
docker-compose up
```

3. Copy the the `mwc/cfg.py.bak` to `mwc/cfg.py` and fill the config values.


4. Install the `mwc` package

```
$ python setup.py install
```

5. Download movies data from IMDB

```
$ mwc sync-imdb
```

6. Download subtitles for the movies

```
$ mwc download-missing-subtitles
```

7. Tweet a random movie

```
$ mwc tweet-movie
```
