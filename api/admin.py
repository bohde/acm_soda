from django.contrib import admin
import acm_soda.api.models as api

for x in api.adminable:
    admin.site.register(x)