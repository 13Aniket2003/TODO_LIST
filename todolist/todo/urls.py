from django.urls import path
from .views import login_view, signup_view, logout_view, HomeView, TodoDetailView

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("", signup_view, name="signup"),
    path("home/", HomeView.as_view(), name="home"),
    path("list/<int:pk>/", TodoDetailView.as_view(), name="todo-detail"),
]