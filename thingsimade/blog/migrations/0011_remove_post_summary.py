# Generated by Django 2.0b1 on 2017-11-20 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20171118_2214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='summary',
        ),
    ]