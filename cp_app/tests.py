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

TEST_USERS = [
{
"username": "someone",
"email": "x@z.hu",
"password": "truthisoutthere"
},
{
"username": "anyone",
"email": "x@z.de",
"password": "noneofyourbusiness"
}
]

TEST_PARTNERS = [
{
"name": "Lapos Elemér",
"city": "Albertirsa",
"address": "Elmebaj u. 999",
"company_name": "Q Kft."
},
{
"name": "Bekő Tóni",
"city": "Kiskunbürgözd",
"address": "Pacsirta u. 72",
"company_name": "Béka Bt."
}
]


class PartnerListTestCase(APITestCase):

    def setUp(self):
        self.url = reverse("partner-list")
        self.client = APIClient()

        self.user = User.objects.create_user(TEST_USERS[0])
        self.user.save()

        self.partner_data = TEST_PARTNERS[0]
        self.partner_data.update({"user": self.user.id})

        self.partner2_data = TEST_PARTNERS[1]
        self.partner2_data.update({"user": self.user.id})


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
        self.assertEqual(partner.user_id, self.partner_data["user"])
        self.assertEqual(partner.name, self.partner_data["name"])
        self.assertEqual(partner.city, self.partner_data["city"])
        self.assertEqual(partner.address, self.partner_data["address"])
        self.assertEqual(partner.company_name, self.partner_data["company_name"])
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

class PartnerDetailTestCase(APITestCase):
    
    def setUp(self):

        self.post_url = reverse("partner-list")
        self.client = APIClient()

        self.user = User.objects.create_user(TEST_USERS[0])
        self.user.save()

        self.partner_data = TEST_PARTNERS[0]
        self.partner_data.update({"user": self.user.id})
        self.partner2_data = TEST_PARTNERS[1]
        self.partner2_data.update({"user": self.user.id})

    def test_partner_get(self):
        """Check a specific partner"""
        self.client.force_authenticate(user=self.user)
        self.client.post(self.post_url, self.partner_data)
        self.client.post(self.post_url, self.partner2_data)

        # Get partner #2

        partners = Partner.objects.get(id=2)
        serializer = PartnerSerializer(partners)

        url = reverse("partner", args=[2])
        response = self.client.get(url)

        self.assertEqual(json.loads(response.content), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Get a nonexistent parner

        url = reverse("partner", args=[4])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Get a deleted parner
        
        self.client.post(self.post_url, self.partner2_data)
        url = reverse("partner", args=[3])
        self.client.delete(url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        



