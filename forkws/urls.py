from django.conf.urls.defaults import *

urlpatterns = patterns('forkws.views',
    url(r'^(?P<id>\d+)/$', 'view_fork', name='view_fork'),
    (r'^$', 'new_page'),
)
