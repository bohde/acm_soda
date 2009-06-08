
from django.shortcuts import render_to_response
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponse, HttpResponseNotAllowed
import django.utils.simplejson as json
from acm_soda.api.models import Inventory, Client
from acm_soda.api.utils import check_signature
from functools import wraps

def dispatch_method(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if request.method != "POST":
            return HttpResponseNotAllowed(['POST'])

        if request.META.get('CONTENT_TYPE', '') != 'application/json':
            return HttpResponseBadRequest('Request must have the content-type "application/json"')

        d = json.loads(request.raw_post_data)

        if not 'signature' in d:
            return HttpResponseBadRequest('Request JSON must include an "signature" element.')

        if not 'client_name' in d:
            return HttpResponseBadRequest('Request JSON must include an "client_name" element.')

        try:
            client = Client.objects.get(name=d.get('client_name'))
        except Client.DoesNotExist:
            return HttpResponseForbidden('Access for that "client_name" is denied.')

        if not check_signature(d, client.auth_key):
            return HttpResponseForbidden('Access for that "client_name" is denied.')

        request.api_client = client

        output = f(request, *args, **kwargs)

        return HttpResponse(json.dumps(output), content_type='application/json')
    return wrapper

@dispatch_method
def inventory_list(request):
    output = []
    for i in Inventory.objects.all():
        output.append(
        {
            'soda': {
                'short_name': i.soda.short_name,
                'description': i.soda.description,
                'cost': i.soda.cost
            },
            'quantity': i.amount
        })
    return output


