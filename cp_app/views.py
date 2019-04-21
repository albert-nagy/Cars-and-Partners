from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework.views import APIView

from cp_app.models import Partner, Car
from cp_app.serializers import PartnerSerializer, UserSerializer, CarSerializer
from django.contrib.auth.models import User

from functools import wraps
from time import time

# Response status codes:

s_201 = status.HTTP_201_CREATED
s_400 = status.HTTP_400_BAD_REQUEST
s_404 = status.HTTP_404_NOT_FOUND

# Authorization decorator:

def authorizeUser(fn):
    @wraps(fn)
    def wrapper(obj, request, *args, **kwargs):
        if request.user.is_authenticated:
            item_model = None

            if isinstance(obj, PartnerDetail):
                item_model = Partner
            elif isinstance(obj, CarDetail):
                item_model = Car

            if item_model is not None:
                try:
                    item = item_model.objects.get(id=args[0])
                    if item.deleted_at > 0:
                        return Response(
                            "The requested item was already deleted",
                            status=s_404
                            )
                    if item.user_id != request.user.id:
                        return Response(
                            "You have no permission to change this item!",
                            status=s_400
                            )
                except item_model.DoesNotExist:
                    return Response(
                    "The requested item was not found",
                    status=s_404
                    )
            response = fn(obj, request, *args)

        else:
            response = Response(
                "This action requires login!",
                status=s_400
                )
        return response
    return wrapper

# Views:

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
            return Response(serializer.data, status=s_201)
        return Response(serializer.errors, status=s_400)

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
            return Response(serializer.data, status=s_201)
        return Response(serializer.errors, status=s_400)

    
class PartnerDetail(APIView):

    def get(self, request, id):
        """Retrieve a particular partner"""
        try:
            partner = Partner.objects.get(id=id, deleted_at=0)
        except Partner.DoesNotExist:
            return HttpResponse(
                "The requested partner was not found",
                status=404
                )

        serializer = PartnerSerializer(partner)
        return JsonResponse(serializer.data)

    @authorizeUser
    def delete(self, request, id):
        """Delete partner"""
        partner = Partner.objects.get(id=id)
        data = {"deleted_at": time()}
        serializer = PartnerSerializer(partner, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=s_201)
        return Response(serializer.errors, status=s_400)
               
class CarList(APIView):

    def get(self, request):
        """List all cars"""
        cars = Car.objects.filter(deleted_at=0).order_by('id')
        serializer = CarSerializer(cars, many=True)
        return JsonResponse(serializer.data, safe=False)

    @authorizeUser
    def post(self, request):
        """Create new car"""
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            try:
                id = Car.objects.latest('id').id +1
            except Car.DoesNotExist:
                id = 1
            user = User.objects.get(id=request.user.id)
            serializer.save(id=id, user=user)
            return Response(serializer.data, status=s_201)
        return Response(serializer.errors, status=s_400)

class CarDetail(APIView):

    def get(self, request, id):
        """Retrieve a particular car"""
        try:
            car = Car.objects.get(id=id, deleted_at=0)
        except Car.DoesNotExist:
            return HttpResponse("The requested car was not found", status=404)

        serializer = CarSerializer(car)
        return JsonResponse(serializer.data)

    @authorizeUser
    def delete(self, request, id):
        """Delete car"""
        car = Car.objects.get(id=id)
        data = {"deleted_at": time()}
        serializer = CarSerializer(car, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=s_201)
        return Response(serializer.errors, status=s_400)