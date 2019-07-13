from bamboolean.factories import interpret
from pyroaring import BitMap
from rest_framework import serializers, generics, viewsets, permissions, authentication
from rest_framework.exceptions import ValidationError

from store.models import Photo, Object


class PhotoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['image']


class PhotoSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ('src', 'width', 'height', 'processed')

    def get_src(self, photo):
        return photo.image.url


LABELS = {
    0: u'__background__',
    1: u'person',
    2: u'bicycle',
    3: u'car',
    4: u'motorcycle',
    5: u'airplane',
    6: u'bus',
    7: u'train',
    8: u'truck',
    9: u'boat',
    10: u'traffic light',
    11: u'fire hydrant',
    12: u'stop sign',
    13: u'parking meter',
    14: u'bench',
    15: u'bird',
    16: u'cat',
    17: u'dog',
    18: u'horse',
    19: u'sheep',
    20: u'cow',
    21: u'elephant',
    22: u'bear',
    23: u'zebra',
    24: u'giraffe',
    25: u'backpack',
    26: u'umbrella',
    27: u'handbag',
    28: u'tie',
    29: u'suitcase',
    30: u'frisbee',
    31: u'skis',
    32: u'snowboard',
    33: u'sports ball',
    34: u'kite',
    35: u'baseball bat',
    36: u'baseball glove',
    37: u'skateboard',
    38: u'surfboard',
    39: u'tennis racket',
    40: u'bottle',
    41: u'wine glass',
    42: u'cup',
    43: u'fork',
    44: u'knife',
    45: u'spoon',
    46: u'bowl',
    47: u'banana',
    48: u'apple',
    49: u'sandwich',
    50: u'orange',
    51: u'broccoli',
    52: u'carrot',
    53: u'hot dog',
    54: u'pizza',
    55: u'donut',
    56: u'cake',
    57: u'chair',
    58: u'couch',
    59: u'potted plant',
    60: u'bed',
    61: u'dining table',
    62: u'toilet',
    63: u'tv',
    64: u'laptop',
    65: u'mouse',
    66: u'remote',
    67: u'keyboard',
    68: u'cell phone',
    69: u'microwave',
    70: u'oven',
    71: u'toaster',
    72: u'sink',
    73: u'refrigerator',
    74: u'book',
    75: u'clock',
    76: u'vase',
    77: u'scissors',
    78: u'teddy bear',
    79: u'hair drier',
    80: u'toothbrush'}


# Cannot `setattr` on a C module, have to subclass
class NegBitMap(BitMap):
    pass


def get_matching_ids(query):
    bitmap_all = BitMap(Photo.objects.values_list("id", flat=True))

    # XXX: hacky
    NegBitMap.__invert__ = lambda self: self ^ bitmap_all

    bitmaps = {l: NegBitMap() for l in LABELS.values()}

    for (photo_id, label) in Object.objects.values_list("photo_id", "label"):
        bitmaps[label].add(photo_id)

    return interpret(query, bitmaps)


class PhotoListView(generics.ListAPIView):
    queryset = Photo.objects.none()
    serializer_class = PhotoSerializer

    def get_queryset(self):
        queryset = Photo.objects.order_by("-uploaded_at").filter(processed=True)

        query = self.request.query_params.get('query', None)
        if query is not None and query != "":
            try:
                matching_ids = get_matching_ids(query)
                queryset = queryset.filter(id__in=matching_ids)
            except Exception as e:
                raise ValidationError(e)

        return queryset


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoUploadSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
