# django_nba_starter

[![Uptime Robot status](https://img.shields.io/uptimerobot/status/m787020082-9e83ac06bbfdca2eeaffe9d1)](https://django-nba-services.herokuapp.com/api/)
[![Uptime Robot ratio (30 days)](https://img.shields.io/uptimerobot/ratio/m787020082-9e83ac06bbfdca2eeaffe9d1)](https://stats.uptimerobot.com/E1wwzTWjDB/787020082)
[![GitHub](https://img.shields.io/github/license/pwelagedara/django_nba_starter)](https://github.com/pwelagedara/django_nba_starter/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/python-v3.9.1-blue)](https://www.python.org/downloads/)
[![GitHub last commit](https://img.shields.io/github/last-commit/pwelagedara/django_nba_starter)](https://github.com/pwelagedara/django_nba_starter/graphs/commit-activity)
[![pwelagedara](https://circleci.com/gh/pwelagedara/django_nba_starter.svg?style=shield)](https://circleci.com/gh/pwelagedara/django_nba_starter)
[![Coverage Status](https://coveralls.io/repos/github/pwelagedara/django_nba_starter/badge.svg?branch=main)](https://coveralls.io/github/pwelagedara/django_nba_starter?branch=main)

This [Django][django] project is a starter project for managing a basketball tournament. Do note that this implementation makes [assumptions](#assumptions) to simplify the implementation.

The code has been deployed [here][deployment] on [Heroku][heroku] backed by a [PostgreSQL][postgresql] database for demonstration purposes. Please refer to [Using the Postman collection](#using-the-postman-collection) to learn how to invoke the APIs.

Be sure to visit my [blog][blog] to check out my other work.

## Table of contents

- [Getting started](#getting-started)
  - [Local development](#local-development)
    - [Using virtual environments( recommended)](#using-virtual-environments-recommended)
    - [Without virtual environments](#without-virtual-environments)
  - [Cloud deployment options](#cloud-deployment-options)
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
- [90th percentile calculation](#90th-percentile-calculation)
- [Performance optimizations](#performance-optimizations)
- [Exception handling](#exception-handling)
- [Assumptions](#assumptions)
- [Known issues](#known-issues)
  - [View migration failure for Postgres on Heroku](#view-migration-failure-for-postgres-on-heroku)
  - [Travis CI build failures](#travis-ci-build-failures)
- [License❗](#license)

## Getting started

If you want to run the project locally pick the local development option here. It is assumed that you have set up your development machine with `git`, `Python`, `pip` and any other dependencies. 

In the cloud deployment section deploying on Heroku and containerized options are discussed.

Pushing the code to the source control triggers a build & deployment pipelines on Heroku and [CircleCI][circleci] respectively. The build pipeline runs the test cases and pushes the test coverage report to the [Coveralls][coveralls] dashboard. The [UptimeRobot][uptimerobot] monitoring dashboard monitors the system status. 

Please click on the `GitHub badges` in the `README.md` to navigate to the aforementioned dashboards. 

![architecture](support/architecture.png?raw=true)

### Local development

When running the application locally the application will point to the [SQLite][sqlite] db. The database with the data is included with the source code to get started without having to run the DDL and DML scripts.

[Helper scripts](#helper-scripts) are provided to prevent having to remember the commands.

#### Using virtual environments( recommended)

Note that you need to have `virtualenv` installed on your machine in addition to the aforementioned dependencies. If you do not have it on your machine please follow the instructions [here][venv] to install it.
Clone the project and `cd` into the project directory.
```shell
git clone https://github.com/pwelagedara/django_nba_starter
cd django_nba_starter
```

Create the virtual environment, activate virtual environment and install the dependencies.
```shell
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

Run the project. Optionally you can load a new dataset.
```shell
python manage.py runserver

# OR use the helper script
./runserver.sh
```

To load the data into SQlite please use the following commands or run [init.sh](init.sh) helper script.
```shell
# Delete existing database
rm -f db.sqlite3

# Make migrations
python manage.py makemigrations

# Make view migrations
python manage.py makeviewmigrations

# Migrate
python manage.py migrate

# Create super user if you want to log into Django admon
python manage.py createsuperuser

# Initialize data using management commands
python manage.py initializedata
```


#### Without virtual environments

### Cloud deployment options
Mention the data generation script
. Also mention the url and credentials( mention that you will share the password seperately) to heroku. 
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
![alt text](support/database-model.png?raw=true)
### Use of database views

## 90th percentile calculation

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

The Project is under [MIT][mit] License. Internet is meant to be free. Use this code anyway you like.

<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

[django]: https://www.djangoproject.com/
[blog]: https://pwelagedara.com
[deployment]: https://django-nba-services.herokuapp.com/api/
[postgresql]: https://www.postgresql.org/
[heroku]: https://www.heroku.com/
[circleci]: https://circleci.com/
[coveralls]: https://coveralls.io/github/pwelagedara/django_nba_starter?branch=main
[uptimerobot]: https://stats.uptimerobot.com/E1wwzTWjDB/787020082
[sqlite]: https://sqlite.org/index.html
[venv]: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
[mit]: https://opensource.org/licenses/MIT
