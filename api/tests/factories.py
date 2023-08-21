# your_app/factories.py

import factory
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}@example.com')
    email = factory.LazyAttribute(lambda obj: obj.username)
    password = factory.PostGenerationMethodCall('set_password', '12345')
