from django.conf.urls.defaults import *

urlpatterns = patterns('acm_soda.api.test_views',
    ('^test$', 'test'),
)