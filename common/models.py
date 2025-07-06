from datetime import datetime
from django.db import models

from common.snowflake import generate_id

class BaseModel(models.Model):
    id = models.BigIntegerField(primary_key=True, default=generate_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        abstract = True

class BaseCacheModel():
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime

    def __init__(self, id=generate_id(), created_at=None, updated_at=None, deleted_at=None):
        self.id = id
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()
        self.deleted_at = deleted_at if deleted_at else None