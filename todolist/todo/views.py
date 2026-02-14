from django.template import loader
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import LoginUser,SignupUser,TodoList, TodoItem

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = None

        try:
            user = SignupUser.objects.get(username=username, is_active = True)
        except SignupUser.DoesNotExist:
            try:
                user = LoginUser.objects.get(username=username, is_active = True)
            except LoginUser.DoesNotExist:
                user = None
        else:
            if user and user.check_password(password):
                messages.success(request, f"Welcome, {username}")
                return redirect("home")
            messages.error(request, "Invalid username or password")       
    return render(request, "login.html")


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get("email")
        password = request.POST.get('password')


        if not username or not email or not password:
            messages.error(request, "All fields are required.")
        elif SignupUser.objects.filter(username = username).exists():
            messages.error(request, "Username already taken")
        elif SignupUser.objects.filter(email = email).exists():
            messages.error(request, "Email already registered.")        
        else:
            new_user = SignupUser(username = username, email = email)
            new_user.set_password(password)
            new_user.save()
            messages.success(request, "Signup successful. you can now log in")
            return redirect("login")
        
    return render(request, "signup.html")



from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.conf import settings

from .models import TodoList, TodoItem

class HomeView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        lists = TodoList.objects.filter(user=request.user)
        edit_list_id = request.GET.get("edit")

        return render(
            request,
            "home.html",
            {
                "lists": lists,
                "edit_list_id": edit_list_id
            }
        )

    def post(self, request):

        if "list_name" in request.POST:
            name = request.POST.get("list_name").strip()
            if name:
                TodoList.objects.create(
                    name=name,
                    user=request.user
                )

        elif "delete_list" in request.POST:
            TodoList.objects.filter(
                id=request.POST.get("delete_list"),
                user=request.user
            ).delete()

        elif "update_list" in request.POST:
            list_id = request.POST.get("update_list")
            new_name = request.POST.get("new_name").strip()

            if new_name:
                TodoList.objects.filter(
                    id=list_id,
                    user=request.user
                ).update(name=new_name)

        return redirect("home")

class TodoDetailView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, pk):
        todo_list = get_object_or_404(
            TodoList,
            id=pk,
            user=request.user
        )
        edit_item_id = request.GET.get("edit")

        return render(
            request,
            "todo_detail.html",
            {
                "list": todo_list,
                "edit_item_id": edit_item_id
            }
        )

    def post(self, request, pk):
        todo_list = get_object_or_404(
            TodoList,
            id=pk,
            user=request.user
        )

        if "item_title" in request.POST:
            title = request.POST.get("item_title").strip()
            if title:
                TodoItem.objects.create(
                    title=title,
                    todo_list=todo_list
                )

        elif "delete_item" in request.POST:
            TodoItem.objects.filter(
                id=request.POST.get("delete_item"),
                todo_list=todo_list
            ).delete()

        elif "update_item" in request.POST:
            item_id = request.POST.get("update_item")
            new_title = request.POST.get("new_title").strip()

            if new_title:
                TodoItem.objects.filter(
                    id=item_id,
                    todo_list=todo_list
                ).update(title=new_title)

        return redirect("todo-detail", pk=pk)
