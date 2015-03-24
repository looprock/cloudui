from fe.models import cloudui_hosts, cloudui_loadbalancers, cloudui_ips, cloudui_hostnames, cloudui_rundeck_jobs
from rest_framework import serializers

class HostSerializer(serializers.HyperlinkedModelSerializer):
#class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = cloudui_hosts
        fields = ('id','cluster_key', 'hostname', 'cloudstack_id', 'release', 'environment', 'product', 'owner', 'tags', 'creation_date')

class LBSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = cloudui_loadbalancers
        fields = ('id','cluster_key', 'cloudstack_id', 'owner', 'tags', 'creation_date')

class IPSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = cloudui_ips
        fields = ('id','cluster_key', 'ipaddr', 'cloudstack_id', 'owner', 'tags', 'creation_date')

class HostnameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = cloudui_hostnames
        fields = ('id','cluster_key', 'hostname', 'ipaddr', 'owner', 'tags', 'creation_date')
