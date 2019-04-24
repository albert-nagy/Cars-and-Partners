import json
from django.urls import reverse
from rest_framework import status

from rest_framework.test import (
    APIClient,
    APITestCase,
    APIRequestFactory,
    force_authenticate
    )

from django.contrib.auth.models import User
from cp_app.models import Partner, Car
from cp_app.serializers import PartnerSerializer, CarSerializer, UserSerializer

# Create your tests here.

class PartnerListTestCase(APITestCase):

    def setUp(self):
        self.url = reverse("partner-list")
        self.client = APIClient()

        self.user = User.objects.create_user(
            "someone",
            "x@z.hu",
            "truthisoutthere"
            )
        self.user.save()

        self.name = "Lapos Elemér"
        self.city = "Albertirsa"
        self.address = "Elmebaj u. 999"
        self.company_name = "Q Kft."

        self.partner_data = {
        "user": self.user.id,
        "name": self.name,
        "city" : self.city,
        "address": self.address,
        "company_name": self.company_name
        }

        self.partner2_data = {
        "user": self.user.id,
        "name": "Bekő Tóni",
        "city" : "Kiskunbürgözd",
        "address": "Pacsirta u. 72",
        "company_name": "Béka Bt."
        }


    def test_create_partner(self):
        """Try to create partner"""

        # First without authentication

        response = self.client.post(self.url, self.partner_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Partner.objects.count(), 0)

        # Then with authentication

        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.partner_data)

        # Check if data got stored correctly

        partner = Partner.objects.get()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Partner.objects.count(), 1)
        self.assertEqual(partner.id, 1)
        self.assertEqual(partner.user_id, self.user.id)
        self.assertEqual(partner.name, self.name)
        self.assertEqual(partner.city, self.city)
        self.assertEqual(partner.address, self.address)
        self.assertEqual(partner.company_name, self.company_name)
        self.assertGreater(partner.created_at, 0)
        self.assertGreater(partner.modify_at, 0)
        self.assertEqual(partner.deleted_at, 0)
        self.assertEqual(len(partner.cars), 0)

    def test_partner_list(self):
        """Check list of partners"""

        # Fill DB with some data
        
        self.client.force_authenticate(user=self.user)
        self.client.post(self.url, self.partner_data)
        self.client.post(self.url, self.partner2_data)

        # Check if data gets displayed correctly

        response = self.client.get(self.url)
        partners = Partner.objects.all()
        self.assertEqual(Partner.objects.count(), 2)
        serializer = PartnerSerializer(partners, many=True)
        self.assertEqual(json.loads(response.content), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)




        



