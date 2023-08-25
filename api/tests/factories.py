# your_app/factories.py

import factory
from django.contrib.auth.models import User, Group
from api.models import Profile, Project, ProjectMedia


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}@example.com")
    email = factory.LazyAttribute(lambda obj: obj.username)
    password = factory.PostGenerationMethodCall("set_password", "12345")


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    phone_number = factory.Sequence(lambda n: 10 * 10 + n)
    avatar_url = factory.Sequence(lambda n: f"http://host/{n}")
    user = factory.SubFactory(UserFactory)


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Sequence(lambda n: f"Name: {n}")
    description = factory.Sequence(lambda n: f"Description: {n}")
    client = factory.SubFactory(UserFactory)
    artist = factory.SubFactory(UserFactory)


class ProjectMediaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectMedia

    file = factory.django.FileField(filename="image.png")
    project = factory.SubFactory(ProjectFactory)
    name = factory.Sequence(lambda n: f"Name: {n}")
