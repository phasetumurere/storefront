from django.db import models
from django.contrib.contenttypes.models import ContentType 
from django.conf import settings
#Allowing Generic relationships like we want to have access to the product $ User without importing it here, 
# for they're totally defferent Apps
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from storefront.settings import AUTH_USER_MODEL

# Create your models here.
class LikedItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)                 
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
