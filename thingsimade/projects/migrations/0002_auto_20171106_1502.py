# Generated by Django 2.0b1 on 2017-11-06 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='summary',
            field=models.CharField(default='lorem ipsum', max_length=140),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(blank=True, max_length=40, unique=True),
        ),
    ]
