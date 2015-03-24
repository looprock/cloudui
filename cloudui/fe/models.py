import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class cloudui_hosts(models.Model):
	cluster_key = models.CharField(max_length=256)
	hostname = models.CharField(max_length=256)
	cloudstack_id = models.CharField(max_length=256)
	owner = models.CharField(max_length=256)
	product = models.CharField(max_length=256)
	release = models.CharField(max_length=256)
	environment = models.CharField(max_length=16)
	tags = models.CharField(max_length=1024,blank=True,default='')
	creation_date = models.DateTimeField('date created')
	def __unicode__(self):              # __unicode__ on Python 2
        	return 'cluster_key: ' +  self.cluster_key + ', hostname: ' + self.hostname + ', cloudstack_id: ' +  self.cloudstack_id + ', owner: ' +  self.owner 

class cloudui_loadbalancers(models.Model):
	cluster_key = models.CharField(max_length=256)
	cloudstack_id = models.CharField(max_length=256)
        owner = models.CharField(max_length=256)
	tags = models.CharField(max_length=1024,blank=True,default='')
	creation_date = models.DateTimeField('date created')
	def __unicode__(self):              # __unicode__ on Python 2
		return 'cluster_key: %s, cloudstack_id: %s, owner: %s' % (self.cluster_key, self.cloudstack_id, self.owner)

class cloudui_ips(models.Model):
	cluster_key = models.CharField(max_length=256)
	cloudstack_id = models.CharField(max_length=256)
	ipaddr = models.CharField(max_length=39)
        owner = models.CharField(max_length=256)
	tags = models.CharField(max_length=1024,blank=True,default='')
	creation_date = models.DateTimeField('date created')
	def __unicode__(self):              # __unicode__ on Python 2
		return 'cluster_key: %s, cloudstack_id: %s, ipaddr: %s, owner: %s' % (self.cluster_key, self.cloudstack_id, self.ipaddr, self.owner)

class cloudui_hostnames(models.Model):
	cluster_key = models.CharField(max_length=256)
	hostname = models.CharField(max_length=256)
	ipaddr = models.CharField(max_length=39)
        owner = models.CharField(max_length=256)
	tags = models.CharField(max_length=1024,blank=True,default='')
	creation_date = models.DateTimeField('date created')
	def __unicode__(self):              # __unicode__ on Python 2
		return 'cluster_key: %s, hostname: %s, ipaddr: %s, owner: %s' % (self.cluster_key, self.hostname, self.ipaddr, self.owner)

class cloudui_rundeck_jobs(models.Model):
	rundeck_name = models.CharField(max_length=256)
	rundeck_id = models.CharField(max_length=64)
	job_enabled = models.BooleanField(default=True)
	def __unicode__(self):
		return 'rundeck_name: %s, rundeck_id: %s, job_enabled: %s' % (self.rundeck_name, self.rundeck_id, str(self.job_enabled))
