from django.urls import path
from rest_framework.authtoken import views

from store.views import PhotoListView, PhotoViewSet

store_urls = [
    path('api-token-auth/', views.obtain_auth_token),
    path('photo/', PhotoViewSet.as_view({'post': 'create'})),
    path('photos/', PhotoListView.as_view())
]
