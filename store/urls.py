from rest_framework import routers

from store.views import PhotoViewSet

store_router = routers.DefaultRouter()
store_router.register(r'photos', PhotoViewSet)