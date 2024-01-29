from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

class AuctionCategory(models.Model):
    category_name = models.CharField(max_length=64)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"{self.category_name} <- {self.parent}"
    
class Listing(models.Model):
    AUCTION_STATUS = [
    ('OP', 'Open'),
    ('CA', 'Canceled'),
    ('SL', 'Sold')
    ]
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=3000)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(AuctionCategory, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='images/')
    status = models.CharField(max_length=2, choices=AUCTION_STATUS, default='OP')
    waching_users = models.ManyToManyField(User, blank=True, related_name="watchlist")

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_date = models.DateTimeField(auto_now_add=True)
    bid_value = models.DecimalField(max_digits=8, decimal_places=2)
    bid_order = models.IntegerField()

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    comment = models.CharField(max_length=1000)
    comment_date = models.DateTimeField(auto_now_add=True)
