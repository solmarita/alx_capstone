from uuid import uuid4
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core import validators

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    review_title = models.CharField(max_length=255, blank=False, null=False)
    review_content = models.TextField(blank=False, null=False)
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=False, null=False, validators=[validators.MinValueValidator(Decimal('1.0')), validators.MaxValueValidator(Decimal('5.0'))])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.review_title} - {self.rating}/5"