from api.models.abstract import WithCreatedUpdated
from django.db import models
from django.contrib.auth import get_user_model
from api.storage import CustomStorage

User = get_user_model()


class Project(WithCreatedUpdated):
    client = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='client_projects', null=True)
    artist = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='artist_projects', null=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f"{self.name} of {self.client}"


class ProjectMedia(WithCreatedUpdated):

    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name="media", null=True)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to='uploads/', storage=CustomStorage())