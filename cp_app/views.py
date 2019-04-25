from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.response import Response

from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from cp_app.models import Partner, Car
from cp_app.serializers import PartnerSerializer, UserSerializer, CarSerializer
from django.contrib.auth.models import User

from functools import wraps
from time import time

# Response status codes:

s_201 = status.HTTP_201_CREATED
s_400 = status.HTTP_400_BAD_REQUEST
s_401 = status.HTTP_401_UNAUTHORIZED
s_404 = status.HTTP_404_NOT_FOUND

# Authorization decorator:


def authorizeUser(fn):
    @wraps(fn)
    def wrapper(obj, request, *args, **kwargs):
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
                        status=s_401
                    )
            except item_model.DoesNotExist:
                return Response(
                    "The requested item was not found",
                    status=s_404
                )
        response = fn(obj, request, *args)
        return response
    return wrapper

# Helper functions:


def save_item(serializer):
    if serializer.is_valid():
        serializer.save()
        return (serializer.data, s_201)
    return (serializer.errors, s_400)

# Views:


class UserAdd(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        response = save_item(serializer)
        return Response(response[0], status=response[1])


class PartnerList(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

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
                id = Partner.objects.latest('id').id + 1
            except Partner.DoesNotExist:
                id = 1
            user = User.objects.get(id=request.user.id)
            serializer.save(id=id, user=user)
            return Response(serializer.data, status=s_201)
        return Response(serializer.errors, status=s_400)


class PartnerDetail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

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
        # If there are connections, archive them by setting their ids negative
        # in the connections list and vice versa
        if len(partner.cars) > 0:
            car_list = [car * -1 if car > 0 else car for car in partner.cars]
            data.update({"cars": car_list})
            cars = Car.objects.filter(id__in=partner.cars)
            for car in cars:
                partner_list = [part * -1 if part ==
                                int(id) else part for part in car.partners]
                car_data = {"partners": partner_list}
                serializer = CarSerializer(car, data=car_data, partial=True)
                response = save_item(serializer)
                if response[1] == s_400:
                    return Response(response[0], status=response[1])
        serializer = PartnerSerializer(partner, data=data, partial=True)
        response = save_item(serializer)
        return Response(response[0], status=response[1])


class CarList(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

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
                id = Car.objects.latest('id').id + 1
            except Car.DoesNotExist:
                id = 1
            user = User.objects.get(id=request.user.id)
            serializer.save(id=id, user=user)
            return Response(serializer.data, status=s_201)
        return Response(serializer.errors, status=s_400)


class CarDetail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

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
        # If there are connections, archive them by setting their ids negative
        # in the connections list and vice versa
        if len(car.partners) > 0:
            partner_list = [partner * -1 if partner >
                            0 else partner for partner in car.partners]
            data.update({"partners": partner_list})
            partners = Partner.objects.filter(id__in=car.partners)
            for partner in partners:
                car_list = [c_id * -1 if c_id ==
                            int(id) else c_id for c_id in partner.cars]
                partner_data = {"cars": car_list}
                serializer = PartnerSerializer(
                    partner,
                    data=partner_data,
                    partial=True
                )
                response = save_item(serializer)
                if response[1] == s_400:
                    return Response(response[0], status=response[1])
        serializer = CarSerializer(car, data=data, partial=True)
        response = save_item(serializer)
        return Response(response[0], status=response[1])

    @authorizeUser
    def patch(self, request, id):
        """Assign partner to a car"""
        car = Car.objects.get(id=id)
        car_partners = car.partners
        partner_id = request.data.get('partner')
        partner = Partner.objects.get(id=partner_id)
        if partner.deleted_at > 0:
            return Response(
                "The requested partner was already deleted",
                status=s_404
            )
        partner_cars = partner.cars

        if partner.user_id == request.user.id:
            if partner_id not in car_partners and id not in partner_cars:
                car_partners.append(partner_id)
                partner_cars.append(id)
                # Save connection car-side
                data = {"partners": car_partners}
                serializer = CarSerializer(
                    car,
                    data=data,
                    partial=True
                )
                response = save_item(serializer)
                # If something went wrong, get an error message right here
                if response[1] == s_400:
                    return Response(response[0], status=response[1])
                # If everything is OK, create dict for final response
                response_data = {}
                response_data.update({"car": response[0]})
                # Save connection partner-side
                data = {"cars": partner_cars}
                serializer = PartnerSerializer(
                    partner,
                    data=data,
                    partial=True
                )
                response = save_item(serializer)
                # If something went wrong here, break
                if response[1] == s_400:
                    return Response(response[0], status=response[1])
                # Otherwise finish and return response
                response_data.update({"partner": response[0]})
                return Response(response_data, status=response[1])
            return Response(
                "Partner was already assigned to this car",
                status=s_400
            )
        return Response(
            "You can only assign your own partners to your cars",
            status=s_401
        )
