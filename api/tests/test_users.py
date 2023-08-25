import rest_framework.test
from rest_framework.test import APITestCase
from django.test import TestCase
from api.tests.factories import UserFactory, GroupFactory, ProfileFactory
from django.urls import reverse
from django.urls import get_resolver
from api.models import User, Profile
import base64


class UserTest(APITestCase):
    def setUp(self):
        self.password = "testpassword"  # will be used in multiple places
        self.user = UserFactory(password=self.password)
        self.group = GroupFactory(name="client")
        self.user.groups.add(self.group)
        self.user.save()

    def perform_auth(self):
        basic_auth_header = (
            "Basic "
            + base64.b64encode(f"{self.user.username}:testpassword".encode()).decode()
        )
        self.client.credentials(HTTP_AUTHORIZATION=basic_auth_header)

    def test_user_endpoint_with_auth(self):
        self.perform_auth()
        url = reverse("users:user-detail", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_user_endpoint_without_auth(self):
        url = reverse("users:user-detail", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 401)

    def test_patch_user_endpoint(self):
        self.perform_auth()
        url = reverse("users:user-detail", kwargs={"pk": self.user.pk})
        data = {"first_name": "patched"}
        response = self.client.patch(url, data)
        user = User.objects.get(email=self.user.email)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(user.first_name, data["first_name"])

    def test_register_endpoint(self):
        url = reverse("auth:register")
        data = {
            "username": "user@example.com",
            "password": "12345",
            "email": "user@example.com",
            "first_name": "string",
            "last_name": "string",
        }
        response = self.client.post(url, data)
        user = User.objects.get(email=data["email"])
        self.assertEquals(user.username, data["username"])
        self.assertEquals(response.status_code, 201)

    def test_register_fails(self):
        """
        user already exists
        """

        url = reverse("auth:register")
        data = {
            "username": self.user.username,
            "password": "12345",
            "email": self.user.username,
            "first_name": "string",
            "last_name": "string",
        }
        response = self.client.post(url, data)
        user_exists = User.objects.filter(email=data["email"]).exists()
        self.assertTrue(user_exists)
        self.assertEquals(response.status_code, 400)

    def test_get_token(self):
        url = reverse("auth:token")

        data = {
            "username": self.user.username,
            "password": self.password,
        }

        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)

    def test_get_user_not_allowed(self):
        self.perform_auth()
        url = reverse("users:user-detail", kwargs={"pk": self.user.pk + 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    #############################################################3
    def test_get_profile(self):
        self.perform_auth()
        profile = ProfileFactory(user=self.user)
        url = reverse("users:profile-list")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()), 1)  # only one profile returned
        self.assertEquals(response.json()[0]["phone_number"], str(profile.phone_number))
        self.assertEquals(response.json()[0]["user"]["email"], self.user.email)

    def test_get_profile_retrieve(self):
        self.perform_auth()
        profile = ProfileFactory(user=self.user)
        url = reverse("users:profile-detail", kwargs={"pk": profile.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()["phone_number"], str(profile.phone_number))
        self.assertEquals(response.json()["user"]["email"], self.user.email)

    def test_post_profile(self):
        self.perform_auth()
        url = reverse("users:profile-list")
        data = {
            "avatar_url": "http://127.0.0.1:8000/admin/api/profile/",
            "phone_number": "1234567890",
        }
        response = self.client.post(url, data)
        profile = Profile.objects.get(user=self.user)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(profile.phone_number, data["phone_number"])
        self.assertEquals(profile.avatar_url, data["avatar_url"])

    def test_post_profile_wrong_avatar_url_format(self):
        self.perform_auth()
        url = reverse("users:profile-list")
        data = {
            "avatar_url": "asd",
            "phone_number": "1234567890",
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 400)

    def test_post_profile_wrong_avatar_phone(self):
        self.perform_auth()
        url = reverse("users:profile-list")
        data = {
            "avatar_url": "asd",
            "phone_number": "123890",
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 400)

    def test_patch_profile(self):
        self.perform_auth()
        profile = ProfileFactory(user=self.user)
        url = reverse("users:profile-detail", kwargs={"pk": profile.pk})
        data = {
            "avatar_url": "http://127.0.0.1:8000/admin/api/profile/",
            "phone_number": "1234567890",
        }
        response = self.client.patch(url, data)
        updated_profile = Profile.objects.get(user=self.user)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(updated_profile.phone_number, data["phone_number"])
        self.assertEquals(updated_profile.avatar_url, data["avatar_url"])


################################################################
