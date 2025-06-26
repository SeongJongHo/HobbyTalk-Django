from django.db import models

from common.snowflake import generate_id

class BaseModel(models.Model):
    id = models.BigIntegerField(primary_key=True, default=generate_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_time = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        abstract = True