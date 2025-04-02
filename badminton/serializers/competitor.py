from rest_framework import serializers
from badminton.models import Competitor, Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'firstname', 'lastname', 'level', 'gender']


class CompetitorSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)

    class Meta:
        model = Competitor
        fields = "__all__"

# class TeamSerializer(serializers.Serializer):
#     """Custom serializer for team data"""
#     # We don't define fields here because we'll handle the data manually


class PairingSerializer(serializers.Serializer):
    """Custom serializer for a pairing of two teams"""
    teamA = serializers.ListField(child=CompetitorSerializer(), required=False)
    teamB = serializers.ListField(child=CompetitorSerializer(), required=False)


class PairingsListSerializer(serializers.Serializer):
    """Serializer for the entire list of pairings"""
    pairings = PairingSerializer(many=True, required=False)

    def to_representation(self, instance):
        """Ensure the returned data matches the serializer's expected structure."""

        return {
            'teamA': [
                CompetitorSerializer(instance['teamA']['a']).data,
                CompetitorSerializer(instance['teamA']['b']).data
            ],
            'teamB': [
                CompetitorSerializer(instance['teamB']['a']).data,
                CompetitorSerializer(instance['teamB']['b']).data
            ],
            'rankDelta': instance["rankDelta"]
        }
