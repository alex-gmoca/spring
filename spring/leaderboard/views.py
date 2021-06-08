from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, action
from rest_framework import viewsets, permissions, status
from django.http import Http404
from django.shortcuts import render
from leaderboard.models import leaderboard_user
from leaderboard.serializers import LeaderboardUserSerializer

def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'scoreboard_users': reverse('user_list', request=request, format=format)
    })

class UserViewSet(viewsets.ModelViewSet):
    """
        retrieve:
        Return the given user.

        list:
        Return a list of all the existing users.

        create:
        Create a new user instance.

        delete:
        Delete a user instance.

        update:
        Update a user instance.

        point_up:
        Adds a point to the given user.

        point_down:
        Removes a point from the given user.
    """
    queryset = leaderboard_user.objects.all()
    serializer_class = LeaderboardUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True)
    def point_up(self, request, *args, **kwargs):
        def get_object(self, pk):
            try:
                user = leaderboard_user.objects.get(pk=pk)
                return user
            except leaderboard_user.DoesNotExist:
                raise Http404
        user = self.get_object()
        user.point_up()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True)
    def point_down(self, request, *args, **kwargs):
        def get_object(self, pk):
            try:
                user = leaderboard_user.objects.get(pk=pk)
                return user
            except leaderboard_user.DoesNotExist:
                raise Http404
        user = self.get_object()
        user.point_down()
        return Response(status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save()