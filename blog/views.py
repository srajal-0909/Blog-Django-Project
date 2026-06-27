from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render , get_object_or_404 , redirect
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Create your views here.



def home(request):
   posts = Post.objects.all().order_by("-created_at")
   paginator = Paginator(posts, 5)  # Show 10 posts per page
   page_number = request.GET.get('page')
   page_obj = paginator.get_page(page_number)
   return render(request,'blog/home.html', {"posts": page_obj})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "blog/post_detail.html", {"post": post})


def create_post(request):
   if request.method == "POST":
      form = PostForm(request.POST)
      if form.is_valid():
         post = form.save(commit=False)
         post.author = request.user
         post.save()
         return redirect("home")
   else:
      form = PostForm()
   return render(request, "blog/create_post.html", {"form": form})


@login_required
def update_post(request, post_id):
   post = get_object_or_404(Post, id=post_id)
   if request.method == "POST":
      form = PostForm(request.POST, instance=post)
      if form.is_valid():
         form.save()
         return redirect("home")
   else:
      form = PostForm(instance=post)
   return render(request, "blog/form.html", {"form": form})
   

@login_required
def delete_post(request, post_id):
   post = get_object_or_404(Post, id=post_id,author = request.user)
   
   if request.method == "POST":
      post.delete()
      return redirect("home")
   return render(request, "blog/delete_post.html", {"post": post})
   

def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username").strip()
        email = request.POST.get("email").strip()
        password = request.POST.get("password")


        if not password:
            messages.error(request, "Password is required.")
            return render(request, "blog/register.html")


        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                "This username is already taken."
            )
            return render(request, "blog/register.html")


        try:
            validate_password(password)

        except ValidationError as e:
            for error in e:
                messages.error(request, error)

            return render(request, "blog/register.html")


        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )


        login(request, user)

        return redirect("home")


    return render(request, "blog/register.html")

def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("home")


    return render(request, "blog/login.html")



def logout_view(request):

    logout(request)

    return redirect("home")   



def profile(request, username):

    user = get_object_or_404(
        User,
        username=username
    )

    posts = Post.objects.filter(
        author=user
    ).order_by("-created_at")


    context = {
        "profile_user": user,
        "posts": posts,
        "post_count": posts.count(),
    }


    return render(
        request,
        "blog/profile.html",
        context
    )