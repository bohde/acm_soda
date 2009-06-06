
from django.conf.urls.defaults import *

urlpatterns = patterns('acm_soda.api.views',
    ('^dispatch$', 'dispatch'),
)
