# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_auto_20180628_1703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='lastupdate_time',
        ),
        migrations.RemoveField(
            model_name='server',
            name='master',
        ),
        migrations.RemoveField(
            model_name='server',
            name='minionid',
        ),
        migrations.RemoveField(
            model_name='server',
            name='salt_ips',
        ),
        migrations.RemoveField(
            model_name='server',
            name='salt_os',
        ),
        migrations.RemoveField(
            model_name='server',
            name='salt_status',
        ),
        migrations.RemoveField(
            model_name='server',
            name='salt_version',
        ),
    ]
