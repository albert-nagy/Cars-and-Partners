from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from cp_app.models import Partner
from cp_app.serializers import PartnerSerializer
from django.contrib.auth.models import User

# Create your views here.
def root(request):
    
    response = {}
    response['logged_in'] = False
    if request.user.is_authenticated():
        response['logged_in'] = True
        response['id'] = request.user.id
        response['username'] = request.user.username
    return JsonResponse(response)

@api_view(['GET', 'POST'])
def partner_list(request):
    """List all partners and create new"""
    if request.method == 'GET':
        partners = Partner.objects.all()
        serializer = PartnerSerializer(partners, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        serializer = PartnerSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=request.user.id)
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def partner_detail(request, id):
    """Retrieve a particular partner"""
    try:
        partner = Partner.objects.get(id=id)
    except Partner.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PartnerSerializer(partner)
        return JsonResponse(serializer.data)

    