from django.contrib import admin

from .models import Photo, Object


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image', 'processed', 'processing')


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Object)