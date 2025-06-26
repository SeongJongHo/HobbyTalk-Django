from django.db import models

from common.models import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'categories'
        
    def __str__(self):
        return self.name