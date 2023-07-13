from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Blog

# Create your views here.

def home(request):
    posts = Blog.objects.all ()
    context = {"posts" : posts}
    return render(request, "app/index.html", context)

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if not username or not email or not password:
            messages.info(request, "Incomplete details")
            return render(request, "app/signup.html")
        user = User.objects.create(username=username, email=email, password=password)
        user.save()
        return redirect(reverse("home"))
    return render(request, "app/signup.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            messages.info(request, "Incomplete details")
            return render(request, "app/login.html")
        user = auth.authenticate(username=username, password=password)
        if not user:
            messages.info(request, "Invalid loggin details")
            return render(request, "app/login.html")
        auth.login(request, user)
        return redirect(reverse("create"))
    return render(request, "app/login.html")

def logout(request):
    auth.logout(request)
    return redirect(reverse("home"))

@login_required
def create(request):
    if request.method == "POST":
        user = request.user
        title = request.POST.get("title")
        category = request.POST.get("category")
        content = request.POST.get("content")
        created = Blog.objects.create(title=title,author=user, category=category, content=content)
        created.save()
        return redirect(reverse("home"))
    return render(request, "app/create.html")

def read (request, id):
    try:
        post = Blog.objects.get (id=id)
        context = {"post": post}
        # show = str(post.content).split()
        # show = show[:4]
        # show = " ".join(show) + " ..."
        # context["show"] = show
    except:
        context= {"post": None}       
    return render (request, "app/read.html", context)

@login_required
def delete (request, id):
    post = Blog.objects.get(id=id)
    if post.author == request.user:
        post.delete()
    return redirect(reverse("home"))

@login_required
def edit (request, id):
    post = Blog.objects.get(id=id)
    context = {"post": post}
    if post.author != request.user:
        messages.info (request, "you are not authorised")
        return redirect(reverse("home"))
    if request.method == "POST":
        title = request.POST.get ("title")
        category= request.POST.get ("category")
        content = request.POST.get ("content")
        img = request.FILES.get("img")
        if img:
            post.image = img
        post.title = title
        post.category = category
        post.content = content
        post.save()
        
        messages.info (request, "Post edited successfully")
        return redirect(reverse("home"))
    return render(request, "app/edit.html", context)

def error(request, exception):
    return render(request, "app/error.html")


def server(request):
    return render(request, "app/server.html")