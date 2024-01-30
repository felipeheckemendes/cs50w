from django.contrib import admin
from . import models

class ListingAdmin(admin.ModelAdmin):
    filter_horizontal = ("watching_users",)

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.AuctionCategory)
admin.site.register(models.Listing, ListingAdmin)
admin.site.register(models.Bid)
admin.site.register(models.Comment)


