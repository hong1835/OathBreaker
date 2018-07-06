#_*_coding:utf-8_*_
from hosts.myauth import UserProfile
from assets import models
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('url', 'name', 'email')


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asset
        #depth=2
        #fields = ('name', 'sn','server','networkdevice')
        fields = ('asset_type', 'idc', 'admin')

class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Server
        #fields = ('name', 'sn','server')