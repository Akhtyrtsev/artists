# your_app/factories.py

import factory
from django.contrib.auth.models import User, Group
from api.models import Profile


class GroupFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Group


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}@example.com')
    email = factory.LazyAttribute(lambda obj: obj.username)
    password = factory.PostGenerationMethodCall('set_password', '12345')


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    phone_number = factory.Sequence(lambda n: 10*10+n)
    avatar_url = factory.Sequence(lambda n: f"http://host/{n}")
    user = factory.SubFactory(UserFactory)