# MovieWordCloud

A Twitter bot that tweets word clouds based on movies scripts.


# How to use

1. Clone this repo

```
$ git clone https://github.com/Bgeninatti/MovieWordCloud.git
```

2. Copy the the `mwc/cfg.py.bak` to `mwc/cfg.py` and fill the config values.


3. Install the `mwc` package

```
$ python setup.py install
```

4. Download movies data from IMDB

```
$ mwc sync-imdb
```

5. Download subtitles for the movies

```
$ mwc download-missing-subtitles
```

6. Tweet a random movie

```
$ mwc tweet-movie
```
