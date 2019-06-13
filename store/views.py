from rest_framework import viewsets, serializers

from store.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()
    width = serializers.SerializerMethodField()
    height = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ('src', 'width', 'height', 'processed')

    def get_src(self, photo):
        request = self.context.get('request')
        return request.build_absolute_uri(photo.image.url)

    def get_width(self, photo):
        return photo.image.width

    def get_height(self, photo):
        return photo.image.height


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.order_by("-uploaded_at")
    serializer_class = PhotoSerializer
