from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import Context, Template, RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from fe.serializers import IPSerializer, LBSerializer, HostSerializer, HostnameSerializer
from fe.models import cloudui_hosts, cloudui_loadbalancers, cloudui_ips, cloudui_hostnames, cloudui_rundeck_jobs

import urllib
import urllib2
from time import sleep
from time import time
from time import strftime
import re

rundeck_endpoint = 'http://rundeck.vast.com:4440'
rundeck_auth = 'xxxx'

# Create your views here.

def index(request):
	if request.user.is_authenticated():
		#x = cloudui_hosts.objects.filter(owner=request.user.username)
		#l = cloudui_loadbalancers.objects.filter(owner=request.user.username)
		#i = cloudui_ips.objects.filter(owner=request.user.username)
		h = cloudui_hostnames.objects.filter(owner=request.user.username).order_by('hostname')
		a = cloudui_hostnames.objects.all().order_by('hostname')
		return render(request, 'index.html', {'owner': request.user.username, 'h': h, 'a': a })
	else:
		output = "please <a href=\"/login/\">login</a>"
		return HttpResponse(output)

def cluster_view(request, ckey):
        if request.user.is_authenticated():
                x = cloudui_hosts.objects.filter(cluster_key=ckey)
                #x = cloudui_hosts.objects.filter(cluster_key=ckey, owner=request.user.username)
                l = cloudui_loadbalancers.objects.filter(cluster_key=ckey)
                #l = cloudui_loadbalancers.objects.filter(cluster_key=ckey, owner=request.user.username)
                i = cloudui_ips.objects.filter(cluster_key=ckey)
                #i = cloudui_ips.objects.filter(cluster_key=ckey, owner=request.user.username)
		h = cloudui_hostnames.objects.filter(cluster_key=ckey)
		#h = cloudui_hostnames.objects.filter(cluster_key=ckey, owner=request.user.username)
		#if len(x) > 0:
                return render(request, 'cluster.html', {'x': x, 'i': i, 'l': l, 'ckey': ckey, 'h': h, 'owner': request.user.username })
		#else:
		#	return HttpResponse('ERROR: Unauthorized to view this resource!')
        else:   
                output = "please <a href=\"/login/\">login</a>"
                return HttpResponse(output)

def hostnames(request):
	if request.user.is_authenticated():
                h = cloudui_hostnames.objects.filter(owner=request.user.username)
                return render(request, 'hostnames.html', { 'h': h })
        else:   
                output = "please <a href=\"/login/\">login</a>"
                return HttpResponse(output)

def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

@api_view(['GET', 'POST', 'DELETE'])
@csrf_exempt
def hosts_api(request):
	if request.method == 'GET':
		hosts = cloudui_hosts.objects.all()
		serializer = HostSerializer(hosts, many=True)
		return Response(serializer.data)
	elif request.method == 'POST':
        	serializer = HostSerializer(data=request.DATA)
        	if serializer.is_valid():
            		serializer.save()
        		return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
        		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
@csrf_exempt
def hosts_api_details(request,pk,format=None):
        if request.method == 'GET':
                host = cloudui_hosts.objects.filter(id=pk)
                serializer = HostSerializer(host, many=True)
                return Response(serializer.data)
        elif request.method == 'DELETE':
                host = cloudui_hosts.objects.filter(id=pk)
                host.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'POST':
		host = cloudui_hosts.objects.filter(id=pk)
                serializer = HostSerializer(host, data=request.DATA, partial=True)
                if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@csrf_exempt
def hosts_api_byname(request,name,format=None):
        if request.method == 'GET':
                host = cloudui_hosts.objects.filter(hostname=name)
                serializer = HostSerializer(host, many=True)
                return Response(serializer.data)

@api_view(['GET'])
@csrf_exempt
def cluster_members(request,ckey,format=None):
        if request.method == 'GET':
                host = cloudui_hosts.objects.filter(cluster_key=ckey)
                serializer = HostSerializer(host, many=True)
                return Response(serializer.data)

@api_view(['GET', 'POST', 'DELETE'])
@csrf_exempt
def hostnames_api(request):
        if request.method == 'GET':
                hostnames = cloudui_hostnames.objects.all()
                serializer = HostnameSerializer(hostnames, many=True)
                return Response(serializer.data)
        elif request.method == 'POST':
                serializer = HostnameSerializer(data=request.DATA)
                if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
@csrf_exempt
def hostnames_api_details(request,pk,format=None):
        if request.method == 'GET':
                x = cloudui_hostnames.objects.filter(id=pk)
                serializer = HostnameSerializer(x, many=True)
                return Response(serializer.data)
        elif request.method == 'DELETE': 
                x = cloudui_hostnames.objects.filter(id=pk)
                x.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'DELETE'])
@csrf_exempt
def lbs_api(request):
        if request.method == 'GET':
                lbs = cloudui_loadbalancers.objects.all()
                serializer = LBSerializer(lbs, many=True)
                return Response(serializer.data)
        elif request.method == 'POST':
                serializer = LBSerializer(data=request.DATA)
                if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@csrf_exempt
def lbs_api_details(request,pk,format=None):
        if request.method == 'GET':
                lbs = cloudui_loadbalancers.objects.filter(id=pk)
                serializer = LBSerializer(lbs, many=True)
                return Response(serializer.data)
        elif request.method == 'DELETE':
		lb = cloudui_loadbalancers.objects.filter(id=pk)
		lb.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'DELETE'])
@csrf_exempt
def ips_api(request):
        if request.method == 'GET':
                ips = cloudui_ips.objects.all()
                serializer = IPSerializer(ips, many=True)
                return Response(serializer.data)
        elif request.method == 'POST':
                serializer = IPSerializer(data=request.DATA)
                if serializer.is_valid():  
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
@csrf_exempt
def ips_api_details(request,pk,format=None):
        if request.method == 'GET':
                x = cloudui_ips.objects.filter(id=pk)
                serializer = IPSerializer(x, many=True)
                return Response(serializer.data)
        elif request.method == 'DELETE':
                x = cloudui_ips.objects.filter(id=pk)
                x.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('login.html', {}, context)

def getrundeckresponse(path):
        headers = {'X-RunDeck-Auth-Token': rundeck_auth}
        url = "%s/%s" % (rundeck_endpoint,path)
        req = urllib2.Request(url, "", headers)
        response = urllib2.urlopen(req)
        return response.read()

def create(request):
        if request.user.is_authenticated():
		context = RequestContext(request)
		if request.method == 'POST':
			release = request.POST['release']
			hostname = request.POST['hostname']
			cobrand = request.POST['cobrand']
			rundeck_job = request.POST['rundeck_job']
                	h = cloudui_hostnames.objects.filter(hostname=hostname)
			if h:
				cheader = 'Oops, hostname %s is already in use. Please pick a different hostname.' % (hostname)
				j = cloudui_rundeck_jobs.objects.filter(job_enabled=True).order_by('rundeck_name')
				#js = sorted(j, key=j.get)
				a = cloudui_hostnames.objects.filter(owner=request.user.username)
				return render_to_response('create.html', {'cheader': cheader, 'j': j, 'a': a}, context)
			elif not re.match('^[a-zA-Z0-9-\.\*]+$',hostname):
				cheader = 'Oops, hostnames must contain only a-Z, 0-9, *, .,  or dashes!'
				j = cloudui_rundeck_jobs.objects.filter(job_enabled=True).order_by('rundeck_name')
				a = cloudui_hostnames.objects.filter(owner=request.user.username)
				return render_to_response('create.html', {'cheader': cheader, 'j': j, 'a': a}, context)
			else:
				headers = {'X-RunDeck-Auth-Token': rundeck_auth}
				if cobrand != "NULL":
					data = "argString=-release %s -hostname %s -user %s -cobrand %s" % (release, hostname, request.user.username, cobrand)
				else:
					data = "argString=-release %s -hostname %s -user %s" % (release, hostname, request.user.username)
  				url = "%s/api/1/job/%s/run" % (rundeck_endpoint, rundeck_job)
  				req = urllib2.Request(url, data, headers)
				response = urllib2.urlopen(req)
				x = response.read()
				xid = x.split("execution id='")[1].split("'")[0]
				return HttpResponseRedirect('/createstatus/%s' % xid)
		else:
			a = cloudui_hostnames.objects.filter(owner=request.user.username)
			j = cloudui_rundeck_jobs.objects.filter(job_enabled=True).order_by('rundeck_name')
			return render_to_response('create.html', {'cheader': '', 'j': j, 'a': a}, context)
        else:   
                output = "please <a href=\"/login/\">login</a>"
                return HttpResponse(output)

def createstatus(request, xid):
	x = getrundeckresponse('api/1/execution/%s' % xid)
	status = x.split("status='")[1].split("'")[0]
	if status == "running":
		resp = "Waiting for response from deployment. Current status: %s" % status
	else:
		resp = "Deploy completed with the status: %s" % (status)
	return render(request, 'createstatus.html', {'resp': resp, 'xid': xid, 'status': status })

def delete(request, ckey):
	if request.user.is_authenticated():
		h = cloudui_hosts.objects.filter(cluster_key=ckey, owner=request.user.username)	
		if h:
			rundeck_job = "07c44a94-89b7-4ef2-a4b4-a52dfb9870e3"
			headers = {'X-RunDeck-Auth-Token': rundeck_auth}
			data = "argString=-cluster %s" % ckey
			url = "%s/api/1/job/%s/run" % (rundeck_endpoint, rundeck_job)
			req = urllib2.Request(url, data, headers)
			response = urllib2.urlopen(req)
			x = response.read()
			xid = x.split("execution id='")[1].split("'")[0]
			#return HttpResponse(str(xid))
			return HttpResponseRedirect('/deletestatus/%s' % xid)
		else:
			output = "ERROR: you don't have permissions to delete cluster %s" % ckey
			return HttpResponse(output)
	else:
		output = "please <a href=\"/login/\">login</a>"
		return HttpResponse(output)

def redeploy(request, ckey):
        if request.user.is_authenticated():
                context = RequestContext(request)
                if request.method == 'POST':
                        release = request.POST['release']
                        product = request.POST['product']
                        myenv = request.POST['myenv']
                	#h = cloudui_hosts.objects.filter(cluster_key=ckey, owner=request.user.username)
                	h = cloudui_hosts.objects.filter(cluster_key=ckey)
                	if h:   
                        	rundeck_job = "62333716-b7a4-4378-87aa-01836d885cd7"
                        	headers = {'X-RunDeck-Auth-Token': rundeck_auth}
                        	data = "argString=-cluster %s -product %s -release %s -environment %s" % (ckey, product, release, myenv)
                        	url = "%s/api/1/job/%s/run" % (rundeck_endpoint, rundeck_job)
                        	req = urllib2.Request(url, data, headers)
                        	response = urllib2.urlopen(req)
                        	x = response.read()
                        	xid = x.split("execution id='")[1].split("'")[0]
                        	#return HttpResponse(str(xid))
                        	return HttpResponseRedirect('/redeploystatus/%s' % xid)
                	else:   
                        	#output = "ERROR: you don't have permissions to redeploy to cluster %s" % ckey
                        	output = "ERROR: cluster %s doesn't exist!" % ckey
                        	return HttpResponse(output)
		else:
			#h = cloudui_hosts.objects.filter(cluster_key=ckey, owner=request.user.username)
			h = cloudui_hosts.objects.filter(cluster_key=ckey)
			return render_to_response('redeploy.html', {'ckey': ckey, 'h': h}, context)
        else:   
                output = "please <a href=\"/login/\">login</a>"
                return HttpResponse(output)

def redeploystatus(request, xid):
        x = getrundeckresponse('api/1/execution/%s' % xid)
        status = x.split("status='")[1].split("'")[0]
        if status == "running":
                resp = "Waiting for response from redeploy. Current status: %s" % status
        else:
                resp = "Redeploy completed with the status: %s" % (status)
        return render(request, 'redeploystatus.html', {'resp': resp, 'xid': xid, 'status': status })

def deletestatus(request, xid):
	x = getrundeckresponse('api/1/execution/%s' % xid)
	status = x.split("status='")[1].split("'")[0]
        if status == "running":
                resp = "Waiting for response from deletion. Current status: %s" % status
        else:
                resp = "Deletion completed with the status: %s" % (status)
        return render(request, 'deletestatus.html', {'resp': resp, 'xid': xid, 'status': status })

def apikeys(request):
        return render(request, 'comingsoon.html', {'name': 'API Keys'})

def databases(request):
        return render(request, 'comingsoon.html', {'name': 'Databases'})

def alerts(request):
        return render(request, 'comingsoon.html', {'name': 'Alerts'})
