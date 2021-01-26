# Generated by Django 3.1.5 on 2021-01-26 02:30

from django.db import migrations
import django_db_views.migration_functions
import django_db_views.operations


class Migration(migrations.Migration):

    dependencies = [
        ('api_services', '0001_initial'),
    ]

    operations = [
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration('SELECT\n        row_number() over () AS id, pid AS player_id, ROUND(AVG(player_score),2) AS player_average \n    FROM\n    (\n        SELECT player_id AS pid, SUM(points) AS player_score \n        FROM api_services_playerscore \n        GROUP BY player_id, game_id\n    ) player_totals GROUP BY pid', 'api_services_playeraveragedbview', engine='django.db.backends.sqlite3'),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration('', 'api_services_playeraveragedbview', engine='django.db.backends.sqlite3'),
            atomic=False,
        ),
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration('SELECT \n        row_number() over () AS id, player_totals.pid AS player_id, pl.team_id,  player_totals.player_score \n    FROM \n    (\n        SELECT player_id AS pid, SUM(points) AS player_score \n        FROM api_services_playerscore \n        GROUP BY player_id, game_id\n    ) player_totals INNER JOIN api_services_player AS pl ON player_totals.pid=pl.user_id', 'api_services_teamplayerscoresdbview', engine='django.db.backends.sqlite3'),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration('', 'api_services_teamplayerscoresdbview', engine='django.db.backends.sqlite3'),
            atomic=False,
        ),
    ]
