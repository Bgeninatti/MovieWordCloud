## 0.2.0 (2021-12-25)

### Refactor

- **opensubtitles**: remove headers from helpers
- **db**: deprecate log
- **queries**: deprecate obsolete imdb query
- **db**: introduce queries module
- introduce db module
- **db**: budget and revenue truncate to 1000 and bigint in DB

### Feat

- **queries**: introduce new query methods
- **cfg**: add FETCH_RANKING_PAGES parameter
- **tmdb**: fetch multiple pages from most populars

### Fix

- **snyc-tmdb**: continue silently if IMDB Id is not available

## 0.1.0 (2021-12-23)

### Refactor

- remove obsolete files
- set credentials in the auth.env file
- deprecate IMDB source (now really)
- deprecate IMDB source (now really)
- use postgres in models instead of sqlite
- add DATABASE_URL con configuration variables
- remove old command scripts
- **cfg**: remove unused cfg
- **namespace**: refactor on namespaces

### Feat

- progress in TMDB integration
- **CLI**: adds subtitles and bots commands to global cli
- **bots**: adds cli for bots module
- **subtitles**: adds cli for subtitles module
- **setup.py**: add setup.py
- **sources**: add sources cli to mwc cli
- **sources**: implements sources cli

### Fix

- do not ignore cfg.py
- fix what was broken
- **twitter-bot**: refactor according new tweepy API
- **imdb**: enable fetching from all rankings
- fix error message in clI

## 0.0.2 (2020-12-05)
