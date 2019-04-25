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

TEST_CARS = [
    {
        "average_fuel": 6.7,
        "driver": "Rozs Réka",
        "owner": "Zab Bence",
        "type": "pr"
    },
    {
        "average_fuel": 110,
        "driver": "Árpa Árpád",
        "owner": "Gondatlan Gazda",
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
        self.assertEqual(
            partner.company_name,
            self.partner_data["company_name"]
        )
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
        self.user2 = User.objects.create_user(TEST_USERS[1])
        self.user2.save()

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

        partner = Partner.objects.get(id=2)
        serializer = PartnerSerializer(partner)

        url = reverse("partner", args=[2])
        response = self.client.get(url)

        self.assertEqual(json.loads(response.content), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Get a nonexistent partner

        url = reverse("partner", args=[99])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Get a deleted partner

        self.client.post(self.post_url, self.partner2_data)
        url = reverse("partner", args=[3])
        self.client.delete(url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partner_delete(self):
        """Try to delete a specific partner"""

        self.client.force_authenticate(user=self.user)
        self.client.post(self.post_url, self.partner_data)

        # First try to delete a partner without any authentication

        self.client.force_authenticate(user=None)

        url = reverse("partner", args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Try to delete a partner

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        partner = Partner.objects.get(id=1)
        self.assertGreater(partner.deleted_at, 0)

        # Try to delete an already deleted partner

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try to delete a partner of another user
        self.client.post(self.post_url, self.partner_data)
        url = reverse("partner", args=[2])

        self.client.force_authenticate(user=self.user2)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Try to delete a nonexistent partner

        url = reverse("partner", args=[99])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CarListTestCase(APITestCase):

    def setUp(self):
        self.url = reverse("car-list")
        self.client = APIClient()

        self.user = User.objects.create_user(TEST_USERS[0])
        self.user.save()
        self.user2 = User.objects.create_user(TEST_USERS[1])
        self.user2.save()

        self.car_data = TEST_CARS[0]
        self.car_data.update({"user": self.user.id})

        self.car2_data = TEST_CARS[1]
        self.car2_data.update({"user": self.user.id})

    def test_create_car(self):
        """Try to create car"""

        # First without authentication

        response = self.client.post(self.url, self.car_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Partner.objects.count(), 0)

        # Then with authentication

        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.car_data)

        # Check if data got stored correctly

        car = Car.objects.get()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 1)
        self.assertEqual(car.id, 1)
        self.assertEqual(car.user_id, self.car_data["user"])
        self.assertEqual(
            float(
                car.average_fuel),
            self.car_data["average_fuel"])
        self.assertEqual(car.driver, self.car_data["driver"])
        self.assertEqual(car.owner, self.car_data["owner"])
        self.assertEqual(car.type, self.car_data["type"])
        self.assertEqual(car.delegation_starting, 0)
        self.assertEqual(car.delegation_ending, 0)
        self.assertGreater(car.created_at, 0)
        self.assertGreater(car.modify_at, 0)
        self.assertEqual(car.deleted_at, 0)
        self.assertEqual(len(car.partners), 0)

    def test_car_list(self):
        """Check list of cars"""

        # Fill DB with some data

        self.client.force_authenticate(user=self.user)
        self.client.post(self.url, self.car_data)

        # Check if data gets displayed correctly

        response = self.client.get(self.url)
        cars = Car.objects.all()
        self.assertEqual(Car.objects.count(), 1)
        serializer = CarSerializer(cars, many=True)
        self.assertEqual(json.loads(response.content), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CarDetailTestCase(APITestCase):

    def setUp(self):

        self.post_url = reverse("car-list")
        self.partner_post_url = reverse("partner-list")
        self.client = APIClient()

        self.user = User.objects.create_user(TEST_USERS[0])
        self.user.save()
        self.user2 = User.objects.create_user(TEST_USERS[1])
        self.user2.save()

        self.car_data = TEST_CARS[0]
        self.car2_data = TEST_CARS[1]

        self.partner_data = TEST_PARTNERS[0]
        self.partner2_data = TEST_PARTNERS[1]

    def test_car_get(self):
        """Check a specific car"""
        self.client.force_authenticate(user=self.user)
        self.client.post(self.post_url, self.car_data)
        self.client.post(self.post_url, self.car2_data)

        # Get car #1

        car = Car.objects.get(id=1)
        serializer = CarSerializer(car)

        url = reverse("car", args=[1])
        response = self.client.get(url)

        self.assertEqual(json.loads(response.content), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Get a nonexistent car

        url = reverse("car", args=[99])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Get a deleted car

        self.client.post(self.post_url, self.car2_data)
        url = reverse("car", args=[3])
        self.client.delete(url)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_car_delete(self):
        """Try to delete a specific car"""

        self.client.force_authenticate(user=self.user)
        self.client.post(self.post_url, self.car_data)

        # First try to delete a car without any authentication

        self.client.force_authenticate(user=None)

        url = reverse("car", args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Try to delete a car

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        car = Car.objects.get(id=1)
        self.assertGreater(car.deleted_at, 0)

        # Try to delete an already deleted car

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try to delete a car of another user
        self.client.post(self.post_url, self.car_data)
        url = reverse("car", args=[2])

        self.client.force_authenticate(user=self.user2)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Try to delete a nonexistent car

        url = reverse("car", args=[99])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_car_patch(self):
        """Try to connect a car with a partner"""
        self.client.force_authenticate(user=self.user)
        self.client.post(self.post_url, self.car_data)
        self.client.post(self.partner_post_url, self.partner_data)

        # Try to make connection without authenticating

        self.client.force_authenticate(user=None)

        url = reverse("car", args=[1])
        data = {"partner": 1}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Try to connect someone else's car

        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Try to connect own car with somwoe else's partner

        self.client.post(self.partner_post_url, self.partner2_data)

        self.client.force_authenticate(user=self.user)
        data = {"partner": 2}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Try to connect a deleted car

        self.client.delete(url)

        data = {"partner": 1}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try to connect car with a deleted partner

        self.client.post(self.post_url, self.car_data)

        partner_url = reverse("partner", args=[1])
        self.client.delete(partner_url)

        url = reverse("car", args=[2])
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try to connect car with partner

        self.client.post(self.partner_post_url, self.partner_data)

        data = {"partner": 3}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        car = Car.objects.get(id=2)
        partner = Partner.objects.get(id=3)
        self.assertIn(3, car.partners)
        self.assertIn(2, partner.cars)

        # Try to make an existing connection again

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteWithConnectionTestCase(APITestCase):

    def setUp(self):

        self.post_url = reverse("car-list")
        self.partner_post_url = reverse("partner-list")
        self.client = APIClient()

        self.user = User.objects.create_user(TEST_USERS[0])
        self.user.save()

        self.car_data = TEST_CARS[0]
        self.car_data.update({"user": self.user.id})
        self.car2_data = TEST_CARS[1]
        self.car2_data.update({"user": self.user.id})

        self.partner_data = TEST_PARTNERS[0]
        self.partner2_data = TEST_PARTNERS[1]

    def test_delete_car_with_connections(self):
        """Delete a car with existing connections"""

        # Create a car and 2 partners

        self.client.force_authenticate(user=self.user)
        self.client.post(self.post_url, self.car_data)
        self.client.post(self.partner_post_url, self.partner_data)
        self.client.post(self.partner_post_url, self.partner2_data)

        # Connect them to each other

        url = reverse("car", args=[1])

        data = {"partner": 1}
        self.client.patch(url, data)
        data = {"partner": 2}
        self.client.patch(url, data)

        # Delete the car

        self.client.delete(url)

        car = Car.objects.get(id=1)

        # Check the negative connection values in the array fields

        self.assertIn(-1, car.partners)
        self.assertIn(-2, car.partners)
        self.assertNotIn(1, car.partners)
        self.assertNotIn(2, car.partners)

        partner1 = Partner.objects.get(id=1)
        partner2 = Partner.objects.get(id=2)

        self.assertIn(-1, partner1.cars)
        self.assertIn(-1, partner2.cars)
        self.assertNotIn(1, partner1.cars)
        self.assertNotIn(1, partner2.cars)

    def test_delete_partner_with_connections(self):
        """Delete a partner with existing connections"""

        # Create a partner and 2 cars

        self.client.force_authenticate(user=self.user)
        self.client.post(self.partner_post_url, self.partner_data)
        self.client.post(self.post_url, self.car_data)
        self.client.post(self.post_url, self.car2_data)

        # Connect them to each other

        data = {"partner": 1}
        url = reverse("car", args=[1])
        self.client.patch(url, data)
        url = reverse("car", args=[2])
        self.client.patch(url, data)

        # Delete the partner

        url = reverse("partner", args=[1])
        self.client.delete(url)

        # Check the negative connection values in the array fields

        partner = Partner.objects.get(id=1)

        self.assertIn(-1, partner.cars)
        self.assertIn(-2, partner.cars)
        self.assertNotIn(1, partner.cars)
        self.assertNotIn(2, partner.cars)

        car1 = Car.objects.get(id=1)
        car2 = Car.objects.get(id=2)

        self.assertIn(-1, car1.partners)
        self.assertIn(-1, car2.partners)
        self.assertNotIn(1, car1.partners)
        self.assertNotIn(1, car2.partners)
