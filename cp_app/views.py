from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from cp_app.models import Partner
from cp_app.serializers import PartnerSerializer, UserSerializer
from django.contrib.auth.models import User
from functools import wraps

# Create your views here.
def authorizeUser(fn):
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        user=request.user.id
        if request.user.is_authenticated:
            response = fn(request)

        else:
            response = Response(
                "This action requires login!", status=status.HTTP_400_BAD_REQUEST)
        return response
    return wrapper

def root(request): 
    response = {}
    response['logged_in'] = False
    if request.user.is_authenticated():
        response['logged_in'] = True
        response['id'] = request.user.id
        response['username'] = request.user.username
    return JsonResponse(response)

@api_view(['POST'])
def user_add(request):
    """Create new user"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def partner_list(request):
    """List all partners"""
    partners = Partner.objects.all()
    serializer = PartnerSerializer(partners, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
@authorizeUser
def partner_add(request):
    """Create new partner"""
    serializer = PartnerSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.get(id=request.user.id)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def partner_detail(request, id):
    """Retrieve a particular partner"""
    try:
        partner = Partner.objects.get(id=id)
    except Partner.DoesNotExist:
        return HttpResponse(status=404)

    serializer = PartnerSerializer(partner)
    return JsonResponse(serializer.data)

    