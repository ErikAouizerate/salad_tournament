from .tournament import TournamentSerializer
from .player import PlayerSerializer
from .competitor import CompetitorSerializer, PairingsListSerializer, CompetitorDetailSerializer
from .club import ClubSerializer

__all__ = [
    'ClubSerializer',
    'TournamentSerializer',
    'PlayerSerializer',
    'PairingsListSerializer',
    'CompetitorSerializer',
    'CompetitorDetailSerializer',
]
