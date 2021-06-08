from leaderboard.views import UserViewSet
from django.urls import path, include
from leaderboard import views
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register(r'leaderboard', views.UserViewSet, basename='leaderboard')


urlpatterns = [
    path('', views.index, name='index'),
    path('', include(router.urls)),
]
