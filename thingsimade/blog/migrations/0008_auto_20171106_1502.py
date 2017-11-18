# Generated by Django 2.0b1 on 2017-11-06 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20171028_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='summary',
            field=models.CharField(default='lorem ipsum', max_length=140),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('D', '✍︎ Draft'), ('U', '⏏︎ Unlisted'), ('P', '✔ Published')], max_length=1),
        ),
    ]