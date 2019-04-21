from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework.views import APIView

from cp_app.models import Partner
from cp_app.serializers import PartnerSerializer, UserSerializer
from django.contrib.auth.models import User

from functools import wraps
from time import time

# Create your views here.
def authorizeUser(fn):
    @wraps(fn)
    def wrapper(obj, request, *args, **kwargs):
        user=request.user.id
        if request.user.is_authenticated:
            response = fn(obj, request, *args)

        else:
            response = Response(
                "This action requires login!",
                status=status.HTTP_400_BAD_REQUEST)
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

class UserAdd(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PartnerList(APIView):

    def get(self, request):
        """List all partners"""
        partners = Partner.objects.filter(deleted_at=0).order_by('id')
        serializer = PartnerSerializer(partners, many=True)
        return JsonResponse(serializer.data, safe=False)

    @authorizeUser
    def post(self, request):
        """Create new partner"""
        serializer = PartnerSerializer(data=request.data)
        if serializer.is_valid():
            try:
                id = Partner.objects.latest('id').id +1
            except Partner.DoesNotExist:
                id = 1
            user = User.objects.get(id=request.user.id)
            serializer.save(id=id, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class PartnerDetail(APIView):

    def get(self, request, id):
        """Retrieve a particular partner"""
        try:
            partner = Partner.objects.get(id=id)
        except Partner.DoesNotExist:
            return HttpResponse("The requested item was not found", status=404)

        serializer = PartnerSerializer(partner)
        return JsonResponse(serializer.data)

    @authorizeUser
    def delete(self, request, id):
        """Delete partner"""
        try:
            partner = Partner.objects.get(id=id)
            if partner.deleted_at == 0:
                data = {"deleted_at": time()}
                serializer = PartnerSerializer(partner, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(
                "The requested item was already deleted",
                status=status.HTTP_404_NOT_FOUND
                )
        except Partner.DoesNotExist:
            return Response(
            "The requested item was not found",
            status=status.HTTP_404_NOT_FOUND
            )
