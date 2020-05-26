from django.db import models
from main_app.models import CustomBaseModel


class Notation(CustomBaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField()