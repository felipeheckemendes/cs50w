from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from . import forms
from .models import User
from . import models
from django.db.models import Max
from django.contrib import messages



def index(request):
    open_listings = models.Listing.objects.filter(status='OP')
    if request.user.is_authenticated:
        watchlist = list(request.user.watchlist.all().values_list('pk', flat=True))
        current_bidder_list = list(request.user.leading_bid_listings.all().values_list('pk', flat=True))
    else:
        watchlist = []
        current_bidder_list = []
    return render(request, "auctions/index.html",{
        "open_listings": open_listings,
        "watchlist": watchlist,
        "current_bidder_list": current_bidder_list,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        form = forms.ListingCreationForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return redirect('index')
        else:
            #If form is not valid, render again the form with the inputs already done, and display error message.
            print(form.errors)
            return render(request, "auctions/create_listing.html",{
                'listing_creation_form': forms.ListingCreationForm(request.POST, request.FILES),
                'error_message': "Something is wrong with your form, please try again."
            })
            
    if request.method == "GET":
        return render(request, "auctions/create_listing.html",{
            'listing_creation_form': forms.ListingCreationForm
        })
    

def listing(request, pk):
    #Listing and bidding winner lists
    if request.user.is_authenticated:
        watchlist = list(request.user.watchlist.all().values_list('pk', flat=True))
        current_bidder_list = list(request.user.leading_bid_listings.all().values_list('pk', flat=True))
    else:
        watchlist = []
        current_bidder_list = []    
    
    #Loads the listing on a variable 'listing', using as reference the primary key pk informed in url
    listing = models.Listing.objects.get(pk=pk)

    #check to see if current user is watching the
    try:
        listing.watching_users.get(username=request.user)
        is_watching = True
    except:
        is_watching = False

    comment_list = models.Comment.objects.filter(listing=listing)

    if request.method == "POST":
        if 'add_watchlist' in request.POST:
            listing.watching_users.add(request.user)
            messages.success(request, 'Item succesfully added to watchlist')
        if 'remove_watchlist' in request.POST:
            messages.success(request, 'Item succesfully removed from watchlist')
            listing.watching_users.remove(request.user)
        if 'make_bid' in request.POST:
            form = forms.BiddingForm(request.POST)
            if form.is_valid():
                bid_value = form.cleaned_data['bid_value']
                if bid_value > listing.starting_bid and (listing.current_bid is None or bid_value > listing.current_bid):
                    listing.current_bid = bid_value
                    listing.current_bidder = request.user
                    listing.save()
                    bidding = form.save(commit=False)
                    bidding.listing = listing
                    bidding.bidder = request.user
                    bidding.bid_value = bid_value
                    if models.Bid.objects.filter(listing=listing).aggregate(Max('bid_order')) is int:
                        bidding.bid_order = models.Bid.objects.filter(listing=listing).aggregate(Max('bid_order'))['bid_order__max'] + 1
                    else:
                        bidding.bid_order = 1
                    bidding.save()
                    messages.success(request, 'Bid succesful.')
                else:
                    messages.error(request, 'Your bid must be higher than current offer.')
        if 'add_comment' in request.POST:
            form = forms.CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.listing = listing
                comment.commenter = request.user
                comment.save()
                messages.success(request, 'Comment added')
        if 'close_auction' in request.POST:
            listing.status = "CL"
            listing.winner = listing.current_bidder
            listing.save()
            

        return redirect('listing', pk=listing.pk)

    elif request.method =="GET":
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "is_watching": is_watching,
            'bidding_form': forms.BiddingForm,
            'comment_form': forms.CommentForm,
            'comment_list': comment_list,
            'watchlist': watchlist,
            'current_bidder_list': current_bidder_list,
        })
    

def watchlist(request):
    if request.user.is_authenticated:
        watchlist = list(request.user.watchlist.all().values_list('pk', flat=True))
        current_bidder_list = list(request.user.leading_bid_listings.all().values_list('pk', flat=True))
    else:
        watchlist = []
        current_bidder_list = []
    return render(request, "auctions/watchlist.html",{
        'watchlist_listings': request.user.watchlist.filter(status='OP'),
        'watchlist': watchlist,
        'current_bidder_list': current_bidder_list,
    })


def categories(request):
    category_list = models.AuctionCategory.objects.all()
    print(category_list)
    return render(request, "auctions/categories.html",{
        'category_list':category_list
    })


def category_listings(request, category_name):
    if request.user.is_authenticated:
        watchlist = list(request.user.watchlist.all().values_list('pk', flat=True))
        current_bidder_list = list(request.user.leading_bid_listings.all().values_list('pk', flat=True))
    else:
        watchlist = []
        current_bidder_list = []
    listings_on_category = models.Listing.objects.filter(category=category_name)
    print(listings_on_category)
    return render(request, "auctions/category_listings.html",{
        'category_name': category_name,
        'listings_on_category': listings_on_category,
        'watchlist': watchlist,
        'current_bidder_list': current_bidder_list,
    })