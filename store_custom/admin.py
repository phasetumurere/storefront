from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdminModel
from tags.models import TaggedItem
from store import models 

# Register your models here.
#Add a Tag on the Product using Generic Relationship
class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    

class CustomProductAdmin(ProductAdminModel):
    inlines = [TagInline]
    

admin.site.unregister(models.Product)
admin.site.register(models.Product, CustomProductAdmin)