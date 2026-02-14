# from django.urls import path
# from .views import login_view, signup_view, logout_view, HomeView, TodoDetailView

# urlpatterns = [
#     path("login/", login_view, name="login"),
#     path("logout/", logout_view, name="logout"),
#     path("", signup_view, name="signup"),
#     path("home/", HomeView.as_view(), name="home"),
#     path("list/<int:pk>/", TodoDetailView.as_view(), name="todo-detail"),
# ]

from django.urls import path
from .views import login_view, signup_view, HomeView, TodoDetailView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", login_view, name="login"),
    path("", signup_view, name="signup"),
    path("home/", HomeView.as_view(), name="home"),
    path("list/<int:pk>/", TodoDetailView.as_view(), name="todo-detail"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]