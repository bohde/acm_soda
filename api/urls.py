from django.conf.urls.defaults import *

"""
I want to know what's in the soda machine. (api/inventory)
I want to know the details of a given soda. (api/inventory/slot)
I want to buy a soda. (api/inventory/soda/buy)
    Decrement amount and charge user account
I want to be able to check my balance. (api/balance)
"""

urlpatterns = patterns('acm_soda.api.views',
    ('^inventory$', 'inventory_list'),
    ('^inventory/(?P<soda>\w+)$','inventory_list'),
    ('^slot/(?P<slot>\d)$', 'slot_inventory'),
)
