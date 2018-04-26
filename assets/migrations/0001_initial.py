# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('asset_type', models.CharField(default=b'server', max_length=64, choices=[(b'server', '\u670d\u52a1\u5668'), (b'networkdevice', '\u7f51\u7edc\u8bbe\u5907'), (b'storagedevice', '\u5b58\u50a8\u8bbe\u5907'), (b'securitydevice', '\u5b89\u5168\u8bbe\u5907'), (b'securitydevice', '\u673a\u623f\u8bbe\u5907'), (b'software', '\u8f6f\u4ef6\u8d44\u4ea7')])),
                ('name', models.CharField(unique=True, max_length=64)),
                ('sn', models.CharField(unique=True, max_length=128, verbose_name='\u8d44\u4ea7SN\u53f7')),
                ('management_ip', models.GenericIPAddressField(null=True, verbose_name='\u7ba1\u7406IP', blank=True)),
                ('trade_date', models.DateField(null=True, verbose_name='\u8d2d\u4e70\u65f6\u95f4', blank=True)),
                ('expire_date', models.DateField(null=True, verbose_name='\u8fc7\u4fdd\u4fee\u671f', blank=True)),
                ('price', models.FloatField(null=True, verbose_name='\u4ef7\u683c', blank=True)),
                ('status', models.SmallIntegerField(default=0, choices=[(0, b'\xe5\x9c\xa8\xe7\xba\xbf'), (1, b'\xe5\xb7\xb2\xe4\xb8\x8b\xe7\xba\xbf'), (2, b'\xe6\x9c\xaa\xe7\x9f\xa5'), (3, b'\xe6\x95\x85\xe9\x9a\x9c'), (4, b'\xe5\xa4\x87\xe7\x94\xa8')])),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u8d44\u4ea7\u603b\u8868',
                'verbose_name_plural': '\u8d44\u4ea7\u603b\u8868',
            },
        ),
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, verbose_name='\u4e1a\u52a1\u7ebf')),
                ('memo', models.CharField(max_length=64, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u4e1a\u52a1\u7ebf',
                'verbose_name_plural': '\u4e1a\u52a1\u7ebf',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(unique=True, max_length=128, verbose_name='\u5408\u540c\u53f7')),
                ('name', models.CharField(max_length=64, verbose_name='\u5408\u540c\u540d\u79f0')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('price', models.IntegerField(verbose_name='\u5408\u540c\u91d1\u989d')),
                ('detail', models.TextField(null=True, verbose_name='\u5408\u540c\u8be6\u7ec6', blank=True)),
                ('start_date', models.DateField(blank=True)),
                ('end_date', models.DateField(blank=True)),
                ('license_num', models.IntegerField(verbose_name='license\u6570\u91cf', blank=True)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u5408\u540c',
                'verbose_name_plural': '\u5408\u540c',
            },
        ),
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cpu_model', models.CharField(max_length=128, verbose_name='CPU\u578b\u53f7', blank=True)),
                ('cpu_count', models.SmallIntegerField(verbose_name='\u7269\u7406cpu\u4e2a\u6570')),
                ('cpu_core_count', models.SmallIntegerField(verbose_name='cpu\u6838\u6570')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'CPU\u90e8\u4ef6',
                'verbose_name_plural': 'CPU\u90e8\u4ef6',
            },
        ),
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(max_length=128, null=True, verbose_name='SN\u53f7', blank=True)),
                ('slot', models.CharField(max_length=64, verbose_name='\u63d2\u69fd\u4f4d')),
                ('manufactory', models.CharField(max_length=64, null=True, verbose_name='\u5236\u9020\u5546', blank=True)),
                ('model', models.CharField(max_length=128, null=True, verbose_name='\u78c1\u76d8\u578b\u53f7', blank=True)),
                ('capacity', models.FloatField(verbose_name='\u78c1\u76d8\u5bb9\u91cfGB')),
                ('iface_type', models.CharField(default=b'SAS', max_length=64, verbose_name='\u63a5\u53e3\u7c7b\u578b', choices=[(b'SATA', b'SATA'), (b'SAS', b'SAS'), (b'SCSI', b'SCSI'), (b'SSD', b'SSD')])),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u786c\u76d8',
                'verbose_name_plural': '\u786c\u76d8',
            },
        ),
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u4e8b\u4ef6\u540d\u79f0')),
                ('event_type', models.SmallIntegerField(verbose_name='\u4e8b\u4ef6\u7c7b\u578b', choices=[(1, '\u786c\u4ef6\u53d8\u66f4'), (2, '\u65b0\u589e\u914d\u4ef6'), (3, '\u8bbe\u5907\u4e0b\u7ebf'), (4, '\u8bbe\u5907\u4e0a\u7ebf'), (5, '\u5b9a\u671f\u7ef4\u62a4'), (6, '\u4e1a\u52a1\u4e0a\u7ebf\\\u66f4\u65b0\\\u53d8\u66f4'), (7, '\u5176\u5b83')])),
                ('component', models.CharField(max_length=255, null=True, verbose_name=b'\xe4\xba\x8b\xe4\xbb\xb6\xe5\xad\x90\xe9\xa1\xb9', blank=True)),
                ('detail', models.TextField(verbose_name='\u4e8b\u4ef6\u8be6\u60c5')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='\u4e8b\u4ef6\u65f6\u95f4')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u4e8b\u4ef6\u7eaa\u5f55',
                'verbose_name_plural': '\u4e8b\u4ef6\u7eaa\u5f55',
            },
        ),
        migrations.CreateModel(
            name='Manufactory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('manufactory', models.CharField(unique=True, max_length=64, verbose_name='\u5382\u5546\u540d\u79f0')),
                ('support_num', models.CharField(max_length=30, verbose_name='\u652f\u6301\u7535\u8bdd', blank=True)),
                ('memo', models.CharField(max_length=128, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u5382\u5546',
                'verbose_name_plural': '\u5382\u5546',
            },
        ),
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sub_asset_type', models.SmallIntegerField(default=0, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(0, b'\xe8\xb7\xaf\xe7\x94\xb1\xe5\x99\xa8'), (1, b'\xe4\xba\xa4\xe6\x8d\xa2\xe6\x9c\xba'), (2, b'\xe8\xb4\x9f\xe8\xbd\xbd\xe5\x9d\x87\xe8\xa1\xa1'), (4, b'VPN\xe8\xae\xbe\xe5\xa4\x87')])),
                ('vlan_ip', models.GenericIPAddressField(null=True, verbose_name='VlanIP', blank=True)),
                ('intranet_ip', models.GenericIPAddressField(null=True, verbose_name='\u5185\u7f51IP', blank=True)),
                ('model', models.CharField(max_length=128, null=True, verbose_name='\u578b\u53f7', blank=True)),
                ('port_num', models.SmallIntegerField(null=True, verbose_name='\u7aef\u53e3\u4e2a\u6570', blank=True)),
                ('device_detail', models.TextField(null=True, verbose_name='\u8bbe\u7f6e\u8be6\u7ec6\u914d\u7f6e', blank=True)),
            ],
            options={
                'verbose_name': '\u7f51\u7edc\u8bbe\u5907',
                'verbose_name_plural': '\u7f51\u7edc\u8bbe\u5907',
            },
        ),
        migrations.CreateModel(
            name='NewAssetApprovalZone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(unique=True, max_length=128, verbose_name='\u8d44\u4ea7SN\u53f7')),
                ('asset_type', models.CharField(blank=True, max_length=64, null=True, choices=[(b'server', '\u670d\u52a1\u5668'), (b'switch', '\u4ea4\u6362\u673a'), (b'router', '\u8def\u7531\u5668'), (b'firewall', '\u9632\u706b\u5899'), (b'storage', '\u5b58\u50a8\u8bbe\u5907'), (b'NLB', 'NetScaler'), (b'wireless', '\u65e0\u7ebfAP'), (b'software', '\u8f6f\u4ef6\u8d44\u4ea7'), (b'others', '\u5176\u5b83\u7c7b')])),
                ('manufactory', models.CharField(max_length=64, null=True, blank=True)),
                ('model', models.CharField(max_length=128, null=True, blank=True)),
                ('ram_size', models.IntegerField(null=True, blank=True)),
                ('cpu_model', models.CharField(max_length=128, null=True, blank=True)),
                ('cpu_count', models.IntegerField(null=True, blank=True)),
                ('cpu_core_count', models.IntegerField(null=True, blank=True)),
                ('os_distribution', models.CharField(max_length=64, null=True, blank=True)),
                ('os_type', models.CharField(max_length=64, null=True, blank=True)),
                ('os_release', models.CharField(max_length=64, null=True, blank=True)),
                ('data', models.TextField(verbose_name='\u8d44\u4ea7\u6570\u636e')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='\u6c47\u62a5\u65e5\u671f')),
                ('approved', models.BooleanField(default=False, verbose_name='\u5df2\u6279\u51c6')),
                ('approved_date', models.DateTimeField(null=True, verbose_name='\u6279\u51c6\u65e5\u671f', blank=True)),
            ],
            options={
                'verbose_name': '\u65b0\u4e0a\u7ebf\u5f85\u6279\u51c6\u8d44\u4ea7',
                'verbose_name_plural': '\u65b0\u4e0a\u7ebf\u5f85\u6279\u51c6\u8d44\u4ea7',
            },
        ),
        migrations.CreateModel(
            name='NIC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, null=True, verbose_name='\u7f51\u5361\u540d', blank=True)),
                ('sn', models.CharField(max_length=128, null=True, verbose_name='SN\u53f7', blank=True)),
                ('model', models.CharField(max_length=128, null=True, verbose_name='\u7f51\u5361\u578b\u53f7', blank=True)),
                ('macaddress', models.CharField(unique=True, max_length=64, verbose_name='MAC')),
                ('ipaddress', models.GenericIPAddressField(null=True, verbose_name='IP', blank=True)),
                ('netmask', models.CharField(max_length=64, null=True, blank=True)),
                ('bonding', models.CharField(max_length=64, null=True, blank=True)),
                ('memo', models.CharField(max_length=128, null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u7f51\u5361',
                'verbose_name_plural': '\u7f51\u5361',
            },
        ),
        migrations.CreateModel(
            name='RaidAdaptor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(max_length=128, null=True, verbose_name='SN\u53f7', blank=True)),
                ('slot', models.CharField(max_length=64, verbose_name='\u63d2\u53e3')),
                ('model', models.CharField(max_length=64, null=True, verbose_name='\u578b\u53f7', blank=True)),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RAM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(max_length=128, null=True, verbose_name='SN\u53f7', blank=True)),
                ('model', models.CharField(max_length=128, verbose_name='\u5185\u5b58\u578b\u53f7')),
                ('slot', models.CharField(max_length=64, verbose_name='\u63d2\u69fd')),
                ('capacity', models.IntegerField(verbose_name='\u5185\u5b58\u5927\u5c0f(MB)')),
                ('memo', models.CharField(max_length=128, null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'RAM',
                'verbose_name_plural': 'RAM',
            },
        ),
        migrations.CreateModel(
            name='SecurityDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sub_asset_type', models.SmallIntegerField(default=0, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(0, b'\xe9\x98\xb2\xe7\x81\xab\xe5\xa2\x99'), (1, b'\xe5\x85\xa5\xe4\xbe\xb5\xe6\xa3\x80\xe6\xb5\x8b\xe8\xae\xbe\xe5\xa4\x87'), (2, b'\xe4\xba\x92\xe8\x81\x94\xe7\xbd\x91\xe7\xbd\x91\xe5\x85\xb3'), (4, b'\xe8\xbf\x90\xe7\xbb\xb4\xe5\xae\xa1\xe8\xae\xa1\xe7\xb3\xbb\xe7\xbb\x9f')])),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sub_asset_type', models.SmallIntegerField(default=0, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(0, b'PC\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8'), (1, b'\xe5\x88\x80\xe7\x89\x87\xe6\x9c\xba'), (2, b'\xe5\xb0\x8f\xe5\x9e\x8b\xe6\x9c\xba')])),
                ('created_by', models.CharField(default=b'auto', max_length=32, choices=[(b'auto', b'Auto'), (b'manual', b'Manual')])),
                ('model', models.CharField(max_length=128, null=True, verbose_name='\u578b\u53f7', blank=True)),
                ('raid_type', models.CharField(max_length=512, null=True, verbose_name='raid\u7c7b\u578b', blank=True)),
                ('os_type', models.CharField(max_length=64, null=True, verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u7c7b\u578b', blank=True)),
                ('os_distribution', models.CharField(max_length=64, null=True, verbose_name='\u53d1\u884c\u7248\u672c', blank=True)),
                ('os_release', models.CharField(max_length=64, null=True, verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u7248\u672c', blank=True)),
            ],
            options={
                'verbose_name': '\u670d\u52a1\u5668',
                'verbose_name_plural': '\u670d\u52a1\u5668',
            },
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sub_asset_type', models.SmallIntegerField(default=0, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(0, b'OS'), (1, b'\xe5\x8a\x9e\xe5\x85\xac\\\xe5\xbc\x80\xe5\x8f\x91\xe8\xbd\xaf\xe4\xbb\xb6'), (2, b'\xe4\xb8\x9a\xe5\x8a\xa1\xe8\xbd\xaf\xe4\xbb\xb6')])),
                ('license_num', models.IntegerField(verbose_name=b'\xe6\x8e\x88\xe6\x9d\x83\xe6\x95\xb0')),
                ('version', models.CharField(help_text='eg. CentOS release 6.5 (Final)', unique=True, max_length=64, verbose_name='\u8f6f\u4ef6/\u7cfb\u7edf\u7248\u672c')),
            ],
            options={
                'verbose_name': '\u8f6f\u4ef6/\u7cfb\u7edf',
                'verbose_name_plural': '\u8f6f\u4ef6/\u7cfb\u7edf',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32, verbose_name=b'Tag name')),
                ('create_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
