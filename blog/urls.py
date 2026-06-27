from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name='home'),
   path("create/", views.create_post, name="create_post"),
   path("post/<int:post_id>/", views.post_detail, name="post_detail"),
   path("post/<int:post_id>/update/", views.update_post, name="update_post"),
   path("post/<int:post_id>/delete/", views.delete_post, name="delete_post"),
   path("login/",views.login_view,name="login"),
   path("logout/",views.logout_view,name="logout"),
   path("register/",views.register_view,name="register"),
   path("profile<str:username>/",views.profile,name="profile"),
   
]
