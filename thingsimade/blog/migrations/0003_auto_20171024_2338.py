# Generated by Django 2.0b1 on 2017-10-24 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='published_date',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='post',
            name='created_date',
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='djangodbmodelsfieldscharfield', max_length=40),
        ),
    ]