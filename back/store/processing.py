import grequests
from django.db import transaction

from store.models import Photo, Object

API_URL = "http://max-object-detector.max.us-south.containers.appdomain.cloud/model/predict"
BATCH_SIZE = 10


def chunks(list_to_split, chunk_size):
    for i in range(0, len(list_to_split), chunk_size):
        yield list_to_split[i:i + chunk_size]


def get_unsent_api_request(photo):
    files = {'image': photo.image.file}
    values = {'threshold': 0.5}

    return grequests.post(API_URL, files=files, data=values)


def save_result(result, photo):
    data = result.json()

    if data['status'] == "ok":
        for p in data['predictions']:
            Object.objects.create(
                photo=photo,
                label=p['label'],
                probability=p['probability'],
                y_min=p['detection_box'][0],
                x_min=p['detection_box'][1],
                y_max=p['detection_box'][2],
                x_max=p['detection_box'][3]
            )

        photo.processed = True
        photo.save()


def process_photos():
    photo_ids = list(Photo.objects.filter(processed=False).values_list('pk', flat=True))

    for photo_ids_chunk in chunks(photo_ids, BATCH_SIZE):
        with transaction.atomic():
            photos = Photo.objects.filter(pk__in=photo_ids_chunk)
            unsent_api_requests = map(get_unsent_api_request, photos)
            results = grequests.map(unsent_api_requests)

            for (r, p) in zip(results, photos):
                save_result(r, p)
