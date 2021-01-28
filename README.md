# django_nba_starter

[![Uptime Robot status](https://img.shields.io/uptimerobot/status/m787020082-9e83ac06bbfdca2eeaffe9d1)](https://django-nba-services.herokuapp.com/api/)
[![Uptime Robot ratio (30 days)](https://img.shields.io/uptimerobot/ratio/m787020082-9e83ac06bbfdca2eeaffe9d1)](https://stats.uptimerobot.com/E1wwzTWjDB/787020082)
[![GitHub](https://img.shields.io/github/license/pwelagedara/django_nba_starter)](https://github.com/pwelagedara/django_nba_starter/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/python-v3.9.1-blue)](https://www.python.org/downloads/)
[![GitHub last commit](https://img.shields.io/github/last-commit/pwelagedara/django_nba_starter)](https://github.com/pwelagedara/django_nba_starter/graphs/commit-activity)
[![pwelagedara](https://circleci.com/gh/pwelagedara/django_nba_starter.svg?style=shield)](https://circleci.com/gh/pwelagedara/django_nba_starter)
[![Coverage Status](https://coveralls.io/repos/github/pwelagedara/django_nba_starter/badge.svg?branch=main)](https://coveralls.io/github/pwelagedara/django_nba_starter?branch=main)

Description goes here... & my contact details( blog & email address).



Fix using reverse in test cases

## Table of contents

- [Getting started](#getting-started)
  - [Local development environment](#local-development-environment)
    - [Using virtual environments](#using-virtual-environments)
    - [Without virtual environments](#without-virtual-environments)
  - [Cloud deployment](#cloud-deployment)
  - [Endpoints](#endpoints)
- [Using the Postman collection](#using-the-postman-collection)
  - [Pre request scripts](#pre-request-scripts)
  - [Postman tests](#postman-tests)
- [Helper scripts](#helper-scripts)
- [Build status](#build-status)
- [Test coverage](#test-coverage)
- [Uptime](#uptime)
- [Database configuration](#database-configuration)
    - [Database model](#database-model)
    - [Use of database views](#use-of-database-views)
- [90th Percentile Calculation](#90th-percentile-calculation)
- [Performance optimizations](#performance-optimizations)
- [Exception handling](#exception-handling)
- [Assumptions](#assumptions)
- [Known issues](#known-issues)
  - [View migration failure for Postgres on Heroku](#view-migration-failure-for-postgres-on-heroku)
  - [Travis CI build failures](#travis-ci-build-failures)
- [License❗](#license)

## Getting started

Mention the data generation script. Also mention the url and credentials( mention that you will share the password seperately) to heroku. 

### Local development environment

#### Using virtual environments
```
pubuduwelagedara@pubudus-MacBook-Air django_nba_starter % python -m venv venv
pubuduwelagedara@pubudus-MacBook-Air django_nba_starter % source ./venv/bin/activate
(venv) pubuduwelagedara@pubudus-MacBook-Air django_nba_starter % python --version
Python 3.9.1
(venv) pubuduwelagedara@pubudus-MacBook-Air django_nba_starter % pip install -r requirements.txt
```
#### Without virtual environments

### Cloud deployment

### Endpoints

## Using the Postman collection

### Pre request scripts

### Postman tests

## Helper scripts

## Build status

## Test coverage

## Uptime

## Database configuration

### Database model

### Use of database views

## 90th Percentile Calculation

## Pagination

## Performance optimizations

## Exception handling

## Assumptions

- If the scores are equal Away Team wins as that team plays with a disadvantage 
- This is a knockout tournament
- Analytics data(`total_time_online`) is captured separately using Google Analytics. It is recorded in minutes in the database
- Super Admin is the Django Super User
- Performance optimization is not a primary concern due to the smaller dataset
- Home Team and Away Team in a game
- Supports one Tournament

## Known issues

### Fix issue with 400 bad request for login endpoint

### View migration failure for Postgres on Heroku

```sql
/**
  
 */
 CREATE VIEW api_services_gamescoresdbview AS
    SELECT
        row_number() over () AS id, game_id, team_id, SUM(player_score) AS team_score
    FROM
    (
        SELECT
            asps.game_id, asps.player_score, asp.team_id
        FROM
        (
            SELECT game_id, player_id, SUM(points) AS player_score
            FROM api_services_playerscore
            GROUP BY player_id, game_id
            ) asps INNER JOIN api_services_player AS asp ON asps.player_id=asp.user_id
    ) tps GROUP BY game_id, team_id
/**
  
 */
CREATE VIEW api_services_playeraveragedbview AS
	SELECT
        apl.player_id, COALESCE(apl.player_average, 0.0) AS player_average,  apisp.team_id
    FROM
    (
        SELECT
            asp.user_id AS player_id, a.player_average AS player_average
        FROM api_services_player AS asp
        LEFT JOIN
        (
            SELECT
                pid AS player_id, ROUND(AVG(player_score),2) AS player_average
            FROM
            (
                SELECT player_id AS pid, SUM(points) AS player_score
                FROM api_services_playerscore
                GROUP BY player_id, game_id
            ) player_totals GROUP BY pid
        ) a ON asp.user_id=a.player_id
    ) apl INNER JOIN api_services_player AS apisp ON apl.player_id=apisp.user_id;

/**
  
 */
CREATE VIEW api_services_teamplayerscoresdbview AS
    SELECT 
        row_number() over () AS id, player_totals.pid AS player_id, pl.team_id,  player_totals.player_score 
    FROM 
    (
        SELECT player_id AS pid, SUM(points) AS player_score 
        FROM api_services_playerscore 
        GROUP BY player_id, game_id
    ) player_totals INNER JOIN api_services_player AS pl ON player_totals.pid=pl.user_id;
```

### Travis CI build failures

```yaml
language: python
python:
  - "3.9"

install:
  - pip install -r requirements.txt

script:
  - coverage run --source=api_services manage.py test --keepdb

after_success:
  - coveralls
```
## License

https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

https://django-nba-services.herokuapp.com
https://www.programmersought.com/article/1055642878/
https://www.programmersought.com/article/6540642829/
