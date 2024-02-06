from django import forms
from . import models

class ListingCreationForm(forms.ModelForm):
    class Meta:
        model = models.Listing
        fields = ['title', 'description', 'starting_bid', 'category', 'image']
        widgets = {
            'description': forms.Textarea
        }

class BiddingForm(forms.ModelForm):
    class Meta:
        model = models.Bid
        fields = ['bid_value']

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['content']
        widgets = {
            'description': forms.Textarea
        }

