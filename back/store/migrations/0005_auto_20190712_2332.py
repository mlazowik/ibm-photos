# Generated by Django 2.2.2 on 2019-07-12 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20190613_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='height',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='width',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
