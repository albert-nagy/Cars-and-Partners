from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from cp_app.models import Partner
from cp_app.serializers import PartnerSerializer

# Create your views here.
def root(request):
    
    response = {}
    response['logged_in'] = False
    if request.user.is_authenticated():
        response['logged_in'] = True
        response['id'] = request.user.id
        response['username'] = request.user.username
    return JsonResponse(response)

@csrf_exempt
def partner_list(request):
    """List all partners"""
    if request.method == 'GET':
        partners = Partner.objects.all()
        serializer = PartnerSerializer(partners, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def partner_detail(request, id):
    """Retrieve a particular partner"""
    try:
        partner = Partner.objects.get(id=id)
    except Partner.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PartnerSerializer(partner)
        return JsonResponse(serializer.data)