from views import dispatch_method
from django.http import HttpResponse

@dispatch_method
def test(request):
    return HttpReponse("test")

test = dispatch_method(test)