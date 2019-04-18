from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def login(request, name, password):
    response = {}
    response['name'] = name
    response['password'] = password
    return JsonResponse(response)