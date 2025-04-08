from django.contrib import admin
from badminton.models import Competitor, Player, Tournament, Partner, Club


@admin.register(Competitor)
class CompetitorAdmin(admin.ModelAdmin):
    list_display = ('id', 'player_firstname', 'player_lastname', 'won', 'lost', 'played', 'player_level', 'rank')

    def player_firstname(self, obj):
        return obj.player.firstname if obj.player else "No Player"
    player_firstname.short_description = "First Name"

    def player_lastname(self, obj):
        return obj.player.lastname if obj.player else "No Player"
    player_lastname.short_description = "Last Name"

    def player_level(self, obj):
        return obj.player.level if obj.player else "N/A"
    player_level.short_description = "Level"


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'a', 'b', 'game_count')


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname')


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
