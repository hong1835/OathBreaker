# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_auto_20180607_1143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='idc',
        ),
    ]
