# Generated by Django 2.0 on 2018-01-02 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20180102_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='gbid',
            field=models.CharField(default=123, max_length=10, unique=True),
            preserve_default=False,
        ),
    ]
