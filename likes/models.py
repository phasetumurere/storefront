from django.db import models
from django.contrib.contenttypes.models import ContentType 
#Allowing Generic relationships like we want to have access to the product $ User without importing it here, 
# for they're totally defferent Apps
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User

# Create your models here.
class LikedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)                 
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
