from rest_framework import serializers
from badminton.models import Competitor, Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'firstname', 'lastname', 'level', 'gender']


class CompetitorDetailSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)

    class Meta:
        model = Competitor
        fields = "__all__"


class CompetitorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Competitor
        fields = "__all__"

# class TeamSerializer(serializers.Serializer):
#     """Custom serializer for team data"""
#     # We don't define fields here because we'll handle the data manually


class PairingSerializer(serializers.Serializer):
    """Custom serializer for a pairing of two teams"""
    teamA = serializers.ListField(child=CompetitorDetailSerializer(), required=False)
    teamB = serializers.ListField(child=CompetitorDetailSerializer(), required=False)


class PairingsListSerializer(serializers.Serializer):
    """Serializer for the entire list of pairings"""
    pairings = PairingSerializer(many=True, required=False)

    def to_representation(self, instance):
        """Ensure the returned data matches the serializer's expected structure."""

        return {
            'teamA': [
                CompetitorDetailSerializer(instance['teamA']['a']).data,
                CompetitorDetailSerializer(instance['teamA']['b']).data
            ],
            'teamB': [
                CompetitorDetailSerializer(instance['teamB']['a']).data,
                CompetitorDetailSerializer(instance['teamB']['b']).data
            ],
            'rankDelta': instance["rankDelta"]
        }
