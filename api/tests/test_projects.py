import rest_framework.test
from rest_framework.test import APITestCase
from django.test import TestCase
from api.tests.factories import UserFactory, GroupFactory, ProfileFactory, ProjectFactory, ProjectMediaFactory
from django.urls import reverse
from django.urls import get_resolver
from api.models import User, Profile, ProjectMedia, Project
from django.core.files.uploadedfile import SimpleUploadedFile
import base64


class ProjectTest(APITestCase):

    def setUp(self):
        self.client_user = UserFactory(username="client@client.com", email="client@client.com", password="pass12345")
        self.artist = UserFactory(username="artist@artist.com", email="artist@artist.com", password="pass12345")
        self.client_group = GroupFactory(name='client')
        self.artist_group = GroupFactory(name='artist')
        self.client_user.groups.add(self.client_group)
        self.artist.groups.add(self.artist_group)
        self.client_user.save()
        self.artist.save()
        self.project = ProjectFactory(artist=self.artist, client=self.client_user)
        self.project_media = ProjectMediaFactory(project=self.project)

    def perform_auth(self, user="client"):
        basic_auth_header = ""
        if user == "client":
            basic_auth_header = 'Basic ' + base64.b64encode(f'{self.client_user.username}:pass12345'.encode()).decode()
        elif user == "artist":
            basic_auth_header = 'Basic ' + base64.b64encode(f'{self.artist.username}:pass12345'.encode()).decode()

        self.client.credentials(HTTP_AUTHORIZATION=basic_auth_header)

    def test_get_client_projects(self):
        self.perform_auth(user="client")
        url = reverse('projects:client-project-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()), 1)
        self.assertTrue('artist' in response.json()[0])
        self.assertTrue('media' in response.json()[0])

    def test_get_client_project(self):
        self.perform_auth(user="client")
        url = reverse('projects:client-project-detail', kwargs={"pk": self.project.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_post_client_project(self):
        self.perform_auth(user="client")
        url = reverse('projects:client-project-list')
        data = {
            "name": "name",
            "description": "description"
        }
        response = self.client.post(url, data=data)
        self.assertEquals(response.status_code, 201)

        projects = Project.objects.filter(client=self.client_user)

        self.assertEquals(projects.count(), 2)
        self.assertEquals(projects.last().name, data["name"])
        self.assertEquals(projects.last().description, data["description"])

    def test_update_client_project(self):

        self.perform_auth(user="client")
        url = reverse('projects:client-project-detail', kwargs={"pk": self.project.pk})
        data = {
            "name": "name",
            "description": "description"
        }
        response = self.client.patch(url, data=data)
        self.assertEquals(response.status_code, 200)

        projects = Project.objects.filter(client=self.client_user)

        self.assertEquals(projects.count(), 1)
        self.assertEquals(projects.last().name, data["name"])
        self.assertEquals(projects.last().description, data["description"])

    def test_delete_client_project(self):

        self.perform_auth(user="client")
        url = reverse('projects:client-project-detail', kwargs={"pk": self.project.pk})
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 204)

        projects = Project.objects.filter(client=self.client_user)

        self.assertEquals(projects.count(), 0)

    def test_get_artist_projects(self):
        self.perform_auth(user="artist")
        url = reverse('projects:artist-project-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()), 1)
        self.assertTrue('client' in response.json()[0])
        self.assertTrue('media' in response.json()[0])

    def test_post_artist_project(self):
        self.perform_auth(user="artist")
        url = reverse('projects:artist-project-list')
        data = {
            "name": "name",
            "description": "description"
        }
        response = self.client.post(url, data=data)
        self.assertEquals(response.status_code, 405)

    def test_post_client_media(self):

        self.perform_auth(user="client")
        url = reverse('projects:upload-media')
        image_content = b'...'  # Binary content of the image
        image = SimpleUploadedFile("test_image.jpg", image_content, content_type="image/jpeg")
        data = {
            "name": "name",
            "project": self.project.pk,
            "file": image
        }
        response = self.client.post(url, data=data)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Project.objects.filter(client=self.client_user).last().media.all().count(), 2)
        self.assertEquals(Project.objects.filter(client=self.client_user).last().media.all().last().name, "name")



