from django.urls import path

from store.views import PhotoListView, PhotoViewSet

store_urls = [
    path('photo/', PhotoViewSet.as_view({'post': 'create'})),
    path('photos/', PhotoListView.as_view())
]
