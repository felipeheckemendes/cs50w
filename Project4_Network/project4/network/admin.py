from django.contrib import admin
from . import models


class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("following",)

class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ("likers",)

# Register your models here.
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Post, PostAdmin)