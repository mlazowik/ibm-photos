from django.urls import path

from store.views import PhotoListView

store_urls = [
    path('photos/', PhotoListView.as_view())
]
