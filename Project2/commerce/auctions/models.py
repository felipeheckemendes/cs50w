from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

class AuctionCategory(models.Model):
    category_name = models.CharField(max_length=64, primary_key=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        parent = f" <- {self.parent}" if self.parent is not None else ""
        return self.category_name + parent
    
class Listing(models.Model):
    AUCTION_STATUS = [
    ('OP', 'Open'),
    ('CA', 'Canceled'),
    ('CL', 'Closed')
    ]
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=3000)
    category = models.ForeignKey(AuctionCategory, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='images/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_listings")
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    current_bid = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    current_bidder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="leading_bid_listings")
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=AUCTION_STATUS, default='OP')
    watching_users = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="won_auctions")

    def __str__(self):
        return f"ID {self.pk} {self.title} |  Status: {self.get_status_display()} | Owner: {self.owner} | Starting bid: {self.starting_bid} | Created in {self.creation_date} | Image {self.image}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_date = models.DateTimeField(auto_now_add=True)
    bid_value = models.DecimalField(max_digits=8, decimal_places=2)
    bid_order = models.IntegerField()

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=1000)
    comment_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.commenter}: {self.content}. ({self.comment_date})"
