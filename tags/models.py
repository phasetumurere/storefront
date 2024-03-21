from django.db import models
from django.contrib.contenttypes.models import ContentType 
#Allowing Generic relationships like we want to have access to the product without importing it here, 
# for they're totally defferent Apps
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)
    
    
class TaggedItem(models.Model):
    # What Tag Applied to what Object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # Type (Product, Video, Article, etc)
    #ID
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
