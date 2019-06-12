from django.db import models


class Photo(models.Model):
    image = models.ImageField()
    uploaded_at = models.DateTimeField('date uploaded', auto_now_add=True)
    processed = models.BooleanField(default=False)


class Object(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    probability = models.FloatField()
    y_min = models.FloatField()
    x_min = models.FloatField()
    y_max = models.FloatField()
    x_max = models.FloatField()
