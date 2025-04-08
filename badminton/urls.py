
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from badminton.views import ClubViewSet, TournamentViewSet, CompetitorViewSet, PlayerViewSet

app_name = 'badminton'

router = DefaultRouter()
router.register(r'tournaments', TournamentViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'competitors', CompetitorViewSet)
router.register(r'clubs', ClubViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
