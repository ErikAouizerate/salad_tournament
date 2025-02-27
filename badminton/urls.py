# from .views import MatchUpView

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TournamentViewSet, PlayerViewSet


# app_name = 'badminton'

# urlpatterns = [
#     path('matchup/', MatchUpView.as_view(), name='matchup'),

# ]

router = DefaultRouter()
router.register(r'tournaments', TournamentViewSet)
router.register(r'players', PlayerViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
