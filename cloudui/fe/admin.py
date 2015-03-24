from django.contrib import admin
from fe.models import cloudui_hosts
from fe.models import cloudui_loadbalancers
from fe.models import cloudui_ips
from fe.models import cloudui_hostnames
from fe.models import cloudui_rundeck_jobs

# Register your models here.
admin.site.register(cloudui_hosts)
admin.site.register(cloudui_loadbalancers)
admin.site.register(cloudui_ips)
admin.site.register(cloudui_hostnames)
admin.site.register(cloudui_rundeck_jobs)
