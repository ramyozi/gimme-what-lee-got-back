from django.contrib import admin
from catalog.models import Category, Item, UserInteraction

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(UserInteraction)
