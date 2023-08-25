from django.core.files.storage import FileSystemStorage
import os


class CustomStorage(FileSystemStorage):
    def __init__(self, location=None, base_url=None):
        if location is None:
            location = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "media"
            )
        if base_url is None:
            base_url = "/media/"
        super().__init__(location, base_url)
