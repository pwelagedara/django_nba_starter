# django_nba_starter

[![Uptime Robot status](https://img.shields.io/uptimerobot/status/m787020082-9e83ac06bbfdca2eeaffe9d1)](https://stats.uptimerobot.com/E1wwzTWjDB/787020082)
[![Uptime Robot ratio (30 days)](https://img.shields.io/uptimerobot/ratio/m787020082-9e83ac06bbfdca2eeaffe9d1)](https://stats.uptimerobot.com/E1wwzTWjDB/787020082)
[![GitHub](https://img.shields.io/github/license/pwelagedara/django_nba_starter)](https://github.com/pwelagedara/django_nba_starter/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/python-v3.9.1-blue)](https://www.python.org/downloads/)
[![GitHub last commit](https://img.shields.io/github/last-commit/pwelagedara/django_nba_starter)](https://github.com/pwelagedara/django_nba_starter/graphs/commit-activity)
[![Build Status](https://travis-ci.com/pwelagedara/django_nba_starter.svg?branch=main)](https://travis-ci.com/pwelagedara/django_nba_starter)
[![Coverage Status](https://coveralls.io/repos/github/pwelagedara/django_nba_starter/badge.svg?branch=main)](https://coveralls.io/github/pwelagedara/django_nba_starter?branch=main)

Description goes here... & my contact details( blog & email address)

## Table of contents

**Table of Contents**

- [Getting started](#getting-started)
- [License❗](#license)

## Getting started

Mention the data generation script

### Local development

#### Without venv

#### Using venv

### Cloud deployment

## Using the Postman collection

## List of helper scripts

### Pre request scripts

### Postman tests

## Build status

## Test coverage

## Uptime

#### Database configuration

## Database model

## 90th Percentile Calculation

### Use of database views

### Performance implications

## Pagination

## Assumptions

- If the scores are equal Away Team wins as that team plays with a disadvantage
- Analytics data(`total_time_online`) is captured separately using Google Analytics 
- Super Admin is the Django Super User
- Performance optimization is not a primary concern due to the smaller dataset
- Home Team and Away Team in a game
- Supports one Tournament

## Known issues

### View migrations failed for Postgres

```sql
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

## License

https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

https://django-nba-services.herokuapp.com
