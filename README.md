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

Be sure to visit my [blog][blog] to find out about my other work.

## Table of contents

- [Getting started](#getting-started)
  - [Local development](#local-development)
    - [Using virtual environments( recommended)❗](#using-virtual-environments-recommended)
    - [Without virtual environments](#without-virtual-environments)
  - [Cloud deployment options](#cloud-deployment-options)
  - [Endpoints](#endpoints)
- [Using the Postman collection❗](#using-the-postman-collection)
  - [Getting started with Postman](#getting-started-with-postman)
  - [Postman tests](#postman-tests)
- [Database configuration](#database-configuration)
    - [Database model](#database-model)
    - [Use of database views](#use-of-database-views)
- [90th percentile calculation](#90th-percentile-calculation)
- [Helper scripts](#helper-scripts)
- [DevOps tools](#devops-tools)
- [Pagination](#pagination)
- [Assumptions](#assumptions)
- [Known issues](#known-issues)
  - [View migration failure for PostgreSQL on Heroku](#view-migration-failure-for-postgresql-on-heroku)
  - [Travis CI build failures](#travis-ci-build-failures)
  - [Login endpoint returns wrong error code](#login-endpoint-returns-wrong-error-code)
- [License❗](#license)

## Getting started

If you want to run the project locally pick the local development option here. It is assumed that you have set up your development machine with `git`, `Python`, `pip` and any other dependencies. 

In the cloud deployment section deploying on Heroku and containerized options are discussed.

Pushing the code to the source control triggers a build & deployment pipelines on Heroku and [CircleCI][circleci] respectively. The build pipeline runs the test cases and pushes the test coverage report to the [Coveralls][coveralls] dashboard. The [UptimeRobot][uptimerobot] monitoring dashboard monitors the system status. 

Please click on the `GitHub badges` in the `README.md` to navigate to the aforementioned dashboards. 

![architecture](support/architecture-v2.png?raw=true)

### Local development

When running the application locally the application will point to the [SQLite][sqlite] db. The database with the data is included with the source code to get started without having to run the DDL and DML scripts.

[Helper scripts](#helper-scripts) are provided to prevent having to remember the commands.

#### Using virtual environments( recommended)

Note that you need to have `virtualenv` installed on your machine in addition to the aforementioned dependencies. If you do not have it on your machine please follow the instructions [here][venv] to install it.

##### ***Step 1:*** Clone the project and `cd` into the project directory.
```shell
git clone https://github.com/pwelagedara/django_nba_starter
cd django_nba_starter
```

##### ***Step 2:*** Create the virtual environment, activate virtual environment and install the dependencies.
```shell
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

##### ***Step 3:*** Run the project. Optionally you can load a new dataset.
```shell
python manage.py runserver

# OR use the helper script
./runserver.sh
```

##### ***Step 2.5 [OPTIONAL]:*** If you want to load new data into SQlite please use the following commands or run [init.sh](init.sh) helper script.
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

> ***NOTE:*** *It has been observed that Django management commands threw errors when executed from a shell script. No attempt has been made to solve the issue. Thus do not use helper scripts here.* 

##### ***Step 1:*** Clone the project and `cd` into the project directory.
```shell
git clone https://github.com/pwelagedara/django_nba_starter
cd django_nba_starter
```

##### ***Step 2:*** Install the dependencies.
```shell
pip install -r requirements.txt
```

##### ***Step 3:*** Run the project. Optionally you can load a new dataset.
```shell
python manage.py runserver
```

##### ***Step 2.5 [OPTIONAL]:*** Follow the instructions [here](#using-virtual-environments-recommended) if you need to load new data.

### Cloud deployment options

The project has been configured to be deployed on Heroku with minimal effort for development purposes. Use heroku commandline to update the database once the database gets created. 

If database views do not get created [run the commands manually](#view-migration-failure-for-postgresql-on-heroku) to create them.

```shell
heroku run python manage.py makemigrations -a APP_NAME
heroku run python manage.py makeviewmigrations -a APP_NAME
heroku run python manage.py migrate -a APP_NAME
heroku run python manage.py createsuperuser -a APP_NAME
heroku run python manage.py initializedata -a APP_NAME
```

For production deployments please follow the checklist [here][checklist].

### Endpoints

> ***NOTE:*** *Django super user is tagged as the super admin. If you have created the super user you can access Django admin panel on http(s)://YOUR_HOST:YOUR_PORT/admin*

| Endpoint             | Authenticated | Authorized user roles             |
|----------------------|---------------|-----------------------------------|
| POST /token          | Yes           | All                               |
| GET /userinfo        | Yes           | All                               |
| GET /tournament      | Yes           | All                               |
| GET /tournament/{id} | Yes           | All                               |
| GET /team            | Yes           | Super admin, admin, coach         |
| GET /team/{id}       | Yes           | Super admin, admin, coach         |
| GET /player          | Yes           | Super admin, admin, coach         |
| GET /player/{id}     | Yes           | Super admin, admin, coach, player |
| GET /admin/user      | Yes           | Super admin, admin                |
| GET /admin/user/{id} | Yes           | Super admin, admin                |

## Using the Postman collection

### Getting started with Postman

Import [DJANGO_NBA_STARTER.postman_collection.json](support/DJANGO_NBA_STARTER.postman_collection.json), [LOCAL.postman_environment.json](support/LOCAL.postman_environment.json) and [HEROKU.postman_environment.json](support/HEROKU.postman_environment.json) into Postman.

A new Postman collection will be available with the name `DJANGO_NBA_STARTER`. Before making any request, pick the Postman environment you want to point to. Note that `token`s and `id`s are automatically assigned as environment variables from previous responses to prevent having to copy values from one request to another.

![architecture](support/postman.png?raw=true)

### Postman tests

All endpoints must return an `HTTP 200 OK` upon successful return. A simple [Postman test][postmantest] is performed to test that.

```javascript
pm.test("HTTP 200 OK", function () {
    pm.response.to.have.status(200);
});
```

## Database configuration

### Database model

The relationships between the database entities are as follows. To see the exact relationship( one to one, one to many etc.) please refer to [models.py](api_services/models.py).

![alt text](support/database.png?raw=true)

### Use of database views

Performing intensive calculations when a request arrives can cause the system to slow down or in the worst case crash. 

Some calculations are performed in the database by using database views to minimize the load.

You may notice that the following database views are getting created in the database in addition to the tables.

- `api_services_gamescoresdbview`
- `api_services_playeraveragedbview`
- `api_services_teamplayerscoresdbview`

## 90th percentile calculation

[Database views](#use-of-database-views) are used to aid the 90th percentile calculation. [NumPy][numpy] is used to obtain the 90th percentile.

> ***NOTE:*** *In order to obtain the top players in the 90th percentile across the team a `top_players` query parameter must be sent. This option is only available for coaches.*

## Helper scripts

Below helper scripts are included in the codebase to facilitate development activities.

- [init.sh](init.sh)
- [migrate.sh](migrate.sh)
- [initializedata.sh](initializedata.sh)
- [runserver.sh](runserver.sh)

## DevOps tools

[Build status][build], [test coverage][coverage] and [uptime][uptimerobot] dashboards are available seperately to provide insights into the system. 

> ***NOTE:*** *`Build status` dashboard is not publicly available.*

## Pagination

Requests returning a list of objects are paginated by design. This decision has been made with the intention to prevent massive server loads. 

Query params `page` and `page_size` can be optionally supplied to set the page and size. 

> ***NOTE:*** *Both `page` and `page_size` parameters must be greater than 0.*

## Assumptions

The following assumptions have been made to facilitate the development of the project.

- This is a knockout tournament.
- There is a home team and an away team in any game. The game is played in the home team's arena.
- If the scores are equal away team wins as that team plays with a disadvantage.
- Analytics data(`total_time_online`, `is_online` etc.) is captured separately using Google Analytics or similar tools. It is recorded in minutes.
- Performance optimization is not a primary concern due to the smaller dataset.
- Only one tournament is supported despite having a `tournament` table in the database.

## Known issues

### View migration failure for PostgreSQL on Heroku

It is observed that the database views do not get created in PostgreSQL on Heroku. If that happens create the database views manually.

The select statements for all [three database views](#use-of-database-views) are available in [models.py](api_services/models.py).

```sql
/**
  api_services_gamescoresdbview
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

```

### Travis CI build failures

Travis CI builds started failing after integrating with Heroku. The build server has been moved from Travis CI to CircleCI due to this issue. The issue has not been thoroughly looked into due to lack of documentation around it apart from a couple of mentions on GitHub issues pages.

### Login endpoint returns wrong error code

It is recommended to respond with an `HTTP 401 UNAUTHORIZED` if the logging in fails. The login endpoint returns an `HTTP 400 BAD REQUEST`. No attempts has been made to correct this as an `HTTP 400 BAD REQUEST` seems acceptable enough.

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
[checklist]: https://docs.djangoproject.com/en/dev/howto/deployment/checklist/
[postmantest]: https://learning.postman.com/docs/writing-scripts/test-scripts/
[numpy]: https://numpy.org/
[build]: https://circleci.com/gh/pwelagedara/django_nba_starter
[coverage]: https://coveralls.io/github/pwelagedara/django_nba_starter?branch=main
[mit]: https://opensource.org/licenses/MIT
