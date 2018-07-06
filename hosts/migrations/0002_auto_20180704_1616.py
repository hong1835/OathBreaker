# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklog',
            name='script_param',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='tasklog',
            name='script_path',
            field=models.TextField(max_length=512, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='tasklog',
            name='script_type',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='operationauditlog',
            name='task_type',
            field=models.CharField(max_length=50, choices=[(b'cmd', b'CMD'), (b'script', b'Script'), (b'file_send', b'\xe5\x8f\x91\xe9\x80\x81\xe6\x96\x87\xe4\xbb\xb6'), (b'file_get', b'\xe4\xb8\x8b\xe8\xbd\xbd\xe6\x96\x87\xe4\xbb\xb6')]),
        ),
        migrations.AlterField(
            model_name='tasklog',
            name='task_type',
            field=models.CharField(max_length=50, choices=[(b'multi_cmd', b'CMD'), (b'multi_script', b'Script'), (b'file_send', b'\xe6\x89\xb9\xe9\x87\x8f\xe5\x8f\x91\xe9\x80\x81\xe6\x96\x87\xe4\xbb\xb6'), (b'file_get', b'\xe6\x89\xb9\xe9\x87\x8f\xe4\xb8\x8b\xe8\xbd\xbd\xe6\x96\x87\xe4\xbb\xb6')]),
        ),
    ]
