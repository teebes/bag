from django.http import HttpResponse

def catch_all(request):
    return HttpResponse('caught')
