from django.contrib import admin
from api_services import models


admin.site.register(models.User)
admin.site.register(models.Admin)
admin.site.register(models.Team)
admin.site.register(models.Player)
admin.site.register(models.Coach)
admin.site.register(models.Tournament)
admin.site.register(models.TournamentRound)
admin.site.register(models.Game)
admin.site.register(models.PlayerScore)
admin.site.register(models.GameScoresDBView)
admin.site.register(models.PlayerAverageDBView)
admin.site.register(models.TeamPlayerScoresDBView)
