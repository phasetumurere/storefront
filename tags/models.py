from django.db import models
from django.contrib.contenttypes.models import ContentType 
#Allowing Generic relationships like we want to have access to the product without importing it here, 
# for they're totally defferent Apps
from django.contrib.contenttypes.fields import GenericForeignKey


#CUnstom Managers
class TaggedItemManager(models.Manager): #This class is best class for all managers
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type) # this stores the ID of the product in ContentType table
        queryset = TaggedItem.objects.\
        select_related('tag').\
        filter(
        content_type = content_type,
        object_id = obj_id        
        )
        # querry = TaggedItem.objects.select_related('tag').filter(
        #     content_type = content_type,
        #     object_id = obj_id
        # )
        return queryset


# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.label
    
    
class TaggedItem(models.Model):
    # What Tag Applied to what Object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # Type (Product, Video, Article, etc)
    #ID
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    #Add objects as an Instance of TaggedItemManager 
    objects = TaggedItemManager()
