from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from fe import views

# Routers provide an easy way of automatically determining the URL conf.
#router = routers.DefaultRouter()
#router.register(r'hosts', views.HostViewSet)
#router.register(r'lbs', views.LBViewSet)
#router.register(r'ips', views.IPViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cloudui.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^fe/', include('fe.urls')),
    url(r'^', include('fe.urls')),
    #url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
