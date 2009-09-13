from django.conf.urls.defaults import *

urlpatterns = patterns('acm_soda.api.test_views',
    ('^test$', 'test'),
)

urlpatterns += patterns('acm_soda.api.views',
    ('^inventory$', 'inventory_list'),
    ('^inventory/(?P<soda>\w+)$','inventory_list'),
    ('^slot/(?P<slot>\d)$', 'slot_inventory'),
)
