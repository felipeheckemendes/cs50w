# --------------------
# Section 0: Imports
# --------------------
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import json
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Post

# ========================
# SECTION 1: Views
# ========================
def index(request):
    return render(request, "network/index.html", {
        'username': request.user.username
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        #Try to validate the form fields according to restrictions on the model
        try:
            #user = User.objects.create_user(username, email, password)
            user = User(username=username, email=email)
            user.set_password(password)
            user.full_clean()
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        except ValidationError as error:
            error_message = '<br>'.join(f"{field}: {', '.join(message for message in message)}" for field, message in error.message_dict.items())
            return render(request, "network/register.html", {
                "message": error_message
            })

        # Attempt to create new user
        #try:
        #    user = User.objects.create_user(username, email, password)
        #    user.save()
        #except IntegrityError:
        #    return render(request, "network/register.html", {
        #        "message": "Username already taken."
        #    })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def user_view(request, user_id):
    user = User.objects.get(username=user_id)
    return render(request, "network/user.html", {
        'username': user,
        'number_of_following': user.following.all().count(),
        'number_of_followers': user.followers.all().count(),
        'is_being_followed': user.followers.filter(username=request.user.username).exists(),
        'is_my_profile': user == request.user,
    })


def following_view(request):
    return render(request, "network/following.html", {
        'username': request.user.username
    })

# ========================
# SECTION 2: APIs
# ========================

@csrf_exempt
def create_post(request):
    # Creating a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Convert POST to python dictionary
    data = json.loads(request.body)
    
    # Check if the content of the post is not None and create the post
    post_content = data.get("post_content")
    if post_content != None:
        post = Post(content=post_content, creator=request.user)
        post.save()
        messages.success(request, "Post created succesfully.")
    else:
        messages.error(request, "Post created succesfully.")
        return JsonResponse({"message": "Post not created. Post must not be blank."}, status=400)
    return JsonResponse({"message": "Post created successfully."}, status=201)


def edit_post(request):
    # Creating a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Convert POST to python dictionary
    data = json.loads(request.body)
    
    # Check if the content of the post is not None and create the post
    post_content = data.get("post_content")
    post_id = data.get("post_id")
    if post_content != None:
        #post = Post(content=post_content, creator=request.user)
        post = Post.objects.get(pk=post_id)
        post.content = post_content
        post.save()
        messages.success(request, "Post edited succesfully.")
    else:
        messages.error(request, "Post must have some content.")
        return JsonResponse({"message": "Post not edited. Post must not be blank."}, status=400)
    return JsonResponse({"message": "Post edited successfully."}, status=201)


def follow(request):
    
    if request.method == "PUT":
        data = json.loads(request.body)
        user = User.objects.get(username=data.get("username"))
        # If request is to 'follow', and user is not following yet: add a follow relation.
        if data.get("follow") == True and not user.followers.filter(username=request.user.username).exists():
            request.user.following.add(user)
        # If request is to 'unlike', and there is 'like' already: remove a new like.
        if data.get("follow") == False and user.followers.filter(username=request.user.username).exists():
            request.user.following.remove(user)
        user.save()
        return HttpResponse(status=204)

@csrf_exempt
def get_posts(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)
    subset = request.GET.get('subset')
    creator = request.GET.get('creator')
    page_number = request.GET.get('page_number', 1)
    print(subset)
    print(creator)
    if subset == "all":
        print('Passou o teste do all')
        posts = Post.objects.all()
    elif subset == "following":
        print("Passou o teste do following")
        following = User.objects.filter(followers=request.user)
        print(following)
        posts = Post.objects.filter(creator__in=following)
        print(posts)
    elif subset == "from_user" and creator != None:
        print("Passou o teste do from user")
        creator = User.objects.get(username=creator)
        print(creator)
        posts = Post.objects.filter(creator=creator)
    else:
        return JsonResponse({"error": "Subset argument should be either 'all', 'following', 'from_user'. If 'from_user', you should specify a username on argument 'creator'"}, status=400)
    
    posts = posts.order_by('-timestamp')
    
    paginator = Paginator(posts, 10)
    page = paginator.get_page(page_number)
    num_pages = paginator.num_pages

    data = {
        'results': [post.serialize(request.user) for post in page],
        'current_page': page_number,
        'total_pages': num_pages
    }

    return JsonResponse(data, safe=False)
    


def like_post(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == "PUT":
        data = json.loads(request.body)
        # If request is to 'like', and there is no 'like' yet: add a new like.
        if data.get("liked") == True and not post.likers.filter(username=request.user.username).exists():
            post.likers.add(User.objects.get(username=request.user.username))
        # If request is to 'unlike', and there is 'like' already: remove a new like.
        if data.get("liked") == False and post.likers.filter(username=request.user.username).exists():
            post.likers.remove(User.objects.get(username=request.user.username))

        post.save()


        return HttpResponse(status=204)

