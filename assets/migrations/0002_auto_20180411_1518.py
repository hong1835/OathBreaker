# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
        ('hosts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='server',
            name='asset',
            field=models.OneToOneField(to='assets.Asset'),
        ),
        migrations.AddField(
            model_name='server',
            name='hosted_on',
            field=models.ForeignKey(related_name='hosted_on_server', blank=True, to='assets.Server', null=True),
        ),
        migrations.AddField(
            model_name='securitydevice',
            name='asset',
            field=models.OneToOneField(to='assets.Asset'),
        ),
        migrations.AddField(
            model_name='ram',
            name='asset',
            field=models.ForeignKey(to='assets.Asset'),
        ),
        migrations.AddField(
            model_name='raidadaptor',
            name='asset',
            field=models.ForeignKey(to='assets.Asset'),
        ),
        migrations.AddField(
            model_name='nic',
            name='asset',
            field=models.ForeignKey(to='assets.Asset'),
        ),
        migrations.AddField(
            model_name='newassetapprovalzone',
            name='approved_by',
            field=models.ForeignKey(verbose_name='\u6279\u51c6\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='networkdevice',
            name='asset',
            field=models.OneToOneField(to='assets.Asset'),
        ),
        migrations.AddField(
            model_name='networkdevice',
            name='firmware',
            field=models.ForeignKey(blank=True, to='assets.Software', null=True),
        ),
        migrations.AddField(
            model_name='eventlog',
            name='asset',
            field=models.ForeignKey(to='assets.Asset'),
        ),
        migrations.AddField(
            model_name='eventlog',
            name='user',
            field=models.ForeignKey(verbose_name='\u4e8b\u4ef6\u6e90', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='disk',
            name='asset',
            field=models.ForeignKey(to='assets.Asset'),
        ),
        migrations.AddField(
            model_name='cpu',
            name='asset',
            field=models.OneToOneField(to='assets.Asset'),
        ),
        migrations.AddField(
            model_name='businessunit',
            name='parent_unit',
            field=models.ForeignKey(related_name='parent_level', blank=True, to='assets.BusinessUnit', null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='admin',
            field=models.ForeignKey(verbose_name='\u8d44\u4ea7\u7ba1\u7406\u5458', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='business_unit',
            field=models.ForeignKey(verbose_name='\u6240\u5c5e\u4e1a\u52a1\u7ebf', blank=True, to='assets.BusinessUnit', null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='contract',
            field=models.ForeignKey(verbose_name='\u5408\u540c', blank=True, to='assets.Contract', null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='idc',
            field=models.ForeignKey(verbose_name='IDC\u673a\u623f', blank=True, to='hosts.IDC', null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='manufactory',
            field=models.ForeignKey(verbose_name='\u5236\u9020\u5546', blank=True, to='assets.Manufactory', null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='tags',
            field=models.ManyToManyField(to='assets.Tag', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='ram',
            unique_together=set([('asset', 'slot')]),
        ),
        migrations.AlterUniqueTogether(
            name='raidadaptor',
            unique_together=set([('asset', 'slot')]),
        ),
        migrations.AlterUniqueTogether(
            name='nic',
            unique_together=set([('asset', 'macaddress')]),
        ),
        migrations.AlterUniqueTogether(
            name='disk',
            unique_together=set([('asset', 'slot')]),
        ),
    ]
