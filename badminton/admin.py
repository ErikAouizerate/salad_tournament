from django.contrib import admin
from badminton.models import Player, User, Tournament, Partner


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'won', 'lost', 'played', 'level', 'rank')


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'a', 'b', 'game_count')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname')


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
