# Generated by Django 2.2.16 on 2020-10-17 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0014_posts_likedby'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followers',
        ),
    ]