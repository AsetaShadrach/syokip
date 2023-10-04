import uuid
from django.db import models
from enum import Enum

class IpStatus(Enum):
    UNALLOCATED='UNALLOCATED'
    ALLOCATED='ALLOCATED'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class IpAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    ip = models.CharField(max_length=50, unique=True)
    subnet = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=40, choices=IpStatus.choices())
    email = models.EmailField(null=True)
    customer_name = models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    last_updated_by = models.CharField(max_length=50, null=True)

    class Meta:
        ordering = ['created_at']


    def __str__(self):
        return f'<IP {str(self.id)}, {self.ip}, {self.email}'