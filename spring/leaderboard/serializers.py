from rest_framework import serializers
from leaderboard.models import leaderboard_user

class LeaderboardUserSerializer(serializers.HyperlinkedModelSerializer):
    points = serializers.ReadOnlyField()
    class Meta:
        model = leaderboard_user
        fields = ['id', 'name', 'age', 'address', 'points','url']
        extra_kwargs = {
            'url': {'view_name': 'leaderboard-detail'}
        }
