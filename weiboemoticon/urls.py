from django.conf.urls import include, url
from django.contrib import admin
from oauth import views
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    url(r'^logout', views.my_logout),
    url(r'^callback', views.oauth_callback, name='callback'),
    url(r'^users', views.all_users),
    #url(r'^posts/')
]