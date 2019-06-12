import requests
from django.db import transaction

from store.models import Photo, Object

API_URL = "http://max-object-detector.max.us-south.containers.appdomain.cloud/model/predict"


def process_photos():
    photo_ids = list(Photo.objects.filter(processed=False).values_list('pk', flat=True))

    session = requests.Session()

    for photo_id in photo_ids:
        with transaction.atomic():
            photo = Photo.objects.get(pk=photo_id)
            files = {'image': photo.image.file}
            values = {'threshold': 0.5}

            r = session.post(API_URL, files=files, data=values)
            data = r.json()

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
