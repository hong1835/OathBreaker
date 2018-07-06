# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_auto_20180608_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='lastupdate_time',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='master',
            field=models.CharField(max_length=64, null=True, verbose_name='master', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='minionid',
            field=models.GenericIPAddressField(unique=True, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='salt_ips',
            field=models.CharField(max_length=128, null=True, verbose_name='IP', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='salt_os',
            field=models.CharField(max_length=64, null=True, verbose_name='OS\u4fe1\u606f', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='salt_status',
            field=models.CharField(max_length=64, null=True, verbose_name='Agent\u72b6\u6001', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='salt_version',
            field=models.CharField(max_length=64, null=True, verbose_name='SaltAgent\u7248\u672c', blank=True),
        ),
    ]
