from rest_framework import serializers
from badminton.models import Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"


# class TeamSerializer(serializers.Serializer):
#     """Custom serializer for team data"""
#     # We don't define fields here because we'll handle the data manually


class PairingSerializer(serializers.Serializer):
    """Custom serializer for a pairing of two teams"""
    teamA = serializers.ListField(child=PlayerSerializer(), required=False)
    teamB = serializers.ListField(child=PlayerSerializer(), required=False)


class PairingsListSerializer(serializers.Serializer):
    """Serializer for the entire list of pairings"""
    pairings = PairingSerializer(many=True, required=False)

    def to_representation(self, instance):
        """Ensure the returned data matches the serializer's expected structure."""

        return {
            'teamA': [
                PlayerSerializer(instance['teamA']['a']).data,
                PlayerSerializer(instance['teamA']['b']).data
            ],
            'teamB': [
                PlayerSerializer(instance['teamB']['a']).data,
                PlayerSerializer(instance['teamB']['b']).data
            ]
        }
