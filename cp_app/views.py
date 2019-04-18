from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def root(request):
    
    response = {}
    response['logged_in'] = False
    if request.user.is_authenticated():
        response['logged_in'] = True
        response['id'] = request.user.id
        response['username'] = request.user.username
    return JsonResponse(response)