
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from badminton.views import TournamentViewSet, PlayerViewSet, UserViewSet, PairingView


app_name = 'badminton'

# urlpatterns = [
#     path('matchup/', MatchUpView.as_view(), name='matchup'),

# ]

router = DefaultRouter()
router.register(r'tournaments', TournamentViewSet)
router.register(r'users', UserViewSet)
router.register(r'players', PlayerViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/pairings', PairingView.as_view(), name='pairing'),
    # path('api/results', Result.as_view(), name='result'),
]
