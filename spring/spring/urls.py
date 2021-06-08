from django.urls import path, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('', include('leaderboard.urls')),
    path('docs/', include_docs_urls(title='Spring API')),
]

urlpatterns += [
    path('', include('rest_framework.urls')),
]