# Generated by Django 2.2.16 on 2020-10-04 15:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_auto_20201003_0906'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='posts',
        ),
        migrations.AlterField(
            model_name='posts',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
