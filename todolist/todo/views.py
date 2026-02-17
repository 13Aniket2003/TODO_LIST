# from django.template import loader
# from django.views import View
# from django.contrib import messages
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import TodoList, TodoItem   #LoginUser,SignupUser,

# from django.contrib.auth import authenticate, login
# from django.shortcuts import render, redirect
# from django.contrib import messages

# # def login_view(request):
# #     next_url = request.GET.get("next") or request.POST.get("next")

# #     if request.method == "POST":
# #         username = request.POST.get("username")
# #         password = request.POST.get("password")

# #         user = authenticate(request, username=username, password=password)

# #         if user is not None:
# #             login(request, user)   # 🔥 CREATES SESSION
# #             return redirect(next_url or "home")
# #         else:
# #             messages.error(request, "Invalid username or password")

# #     return render(request, "login.html", {"next": next_url})

# # from django.contrib.auth.models import User

# # def signup_view(request):
# #     if request.method == "POST":
# #         username = request.POST.get("username")
# #         email = request.POST.get("email")
# #         password = request.POST.get("password")

# #         if User.objects.filter(username=username).exists():
# #             messages.error(request, "Username already taken")
# #         else:
# #             User.objects.create_user(
# #                 username=username,
# #                 email=email,
# #                 password=password
# #             )
# #             messages.success(request, "Signup successful. Please login.")
# #             return redirect("login")

# #     return render(request, "signup.html")

# from django.contrib.auth import authenticate, login

# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(request, username=username, password=password)

#         if user:
#             login(request, user)
#             return redirect("home")
#         else:
#             messages.error(request, "Invalid username or password")

#     return render(request, "login.html")



# from django.contrib.auth.models import User

# def signup_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists")
#         else:
#             User.objects.create_user(
#                 username=username,
#                 email=email,
#                 password=password
#             )
#             messages.success(request, "Account created. Please login.")
#             return redirect("login")

#     return render(request, "signup.html")



# from django.contrib.auth import logout

# def logout_view(request):
#     logout(request)
#     return redirect("login")



# from django.shortcuts import render, redirect, get_object_or_404
# from django.views import View
# from django.contrib import messages
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.mail import send_mail
# from django.conf import settings

# from .models import TodoList, TodoItem

# class HomeView(LoginRequiredMixin, View):
#     login_url = "login"

#     def get(self, request):
#         lists = TodoList.objects.filter(user=request.user)
#         edit_list_id = request.GET.get("edit")

#         return render(
#             request,
#             "home.html",
#             {
#                 "lists": lists,
#                 "edit_list_id": edit_list_id
#             }
#         )

#     def post(self, request):

#         if "list_name" in request.POST:
#             name = request.POST.get("list_name").strip()
#             if name:
#                 TodoList.objects.create(
#                     name=name,
#                     user=request.user
#                 )

#         elif "delete_list" in request.POST:
#             TodoList.objects.filter(
#                 id=request.POST.get("delete_list"),
#                 user=request.user
#             ).delete()

#         elif "update_list" in request.POST:
#             list_id = request.POST.get("update_list")
#             new_name = request.POST.get("new_name").strip()

#             if new_name:
#                 TodoList.objects.filter(
#                     id=list_id,
#                     user=request.user
#                 ).update(name=new_name)

#         return redirect("home")

# class TodoDetailView(LoginRequiredMixin, View):
#     login_url = "login"

#     def get(self, request, pk):
#         todo_list = get_object_or_404(
#             TodoList,
#             id=pk,
#             user=request.user
#         )
#         edit_item_id = request.GET.get("edit")

#         return render(
#             request,
#             "todo_detail.html",
#             {
#                 "list": todo_list,
#                 "edit_item_id": edit_item_id
#             }
#         )

#     def post(self, request, pk):
#         todo_list = get_object_or_404(
#             TodoList,
#             id=pk,
#             user=request.user
#         )

#         if "item_title" in request.POST:
#             title = request.POST.get("item_title").strip()
#             if title:
#                 TodoItem.objects.create(
#                     title=title,
#                     todo_list=todo_list
#                 )

#         elif "delete_item" in request.POST:
#             TodoItem.objects.filter(
#                 id=request.POST.get("delete_item"),
#                 todo_list=todo_list
#             ).delete()

#         elif "update_item" in request.POST:
#             item_id = request.POST.get("update_item")
#             new_title = request.POST.get("new_title").strip()

#             if new_title:
#                 TodoItem.objects.filter(
#                     id=item_id,
#                     todo_list=todo_list
#                 ).update(title=new_title)

#         return redirect("todo-detail", pk=pk)







from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import TodoList, TodoItem


from .utils import send_email

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # ✅ SEND LOGIN ALERT EMAIL
            send_email(
                user.email,
                "Login Alert",
                f"Hi {user.username}, you logged in successfully."
            )

            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


from .utils import send_email

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # ✅ SEND SIGNUP EMAIL (NON-BLOCKING)
            send_email(
                email,
                "Welcome to Todo App",
                f"Hi {username}, your account has been created successfully."
            )

            messages.success(request, "Account created. Please login.")
            return redirect("login")

    return render(request, "signup.html")

def logout_view(request):
    logout(request)
    return redirect("login")


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

        # ✅ PREVENT DUPLICATE TODO LIST
        if "list_name" in request.POST:
            name = request.POST.get("list_name").strip()

            if name:
                exists = TodoList.objects.filter(
                    user=request.user,
                    name__iexact=name
                ).exists()

                if exists:
                    messages.error(request, "Todo list already exists")
                else:
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
                exists = TodoList.objects.filter(
                    user=request.user,
                    name__iexact=new_name
                ).exclude(id=list_id).exists()

                if exists:
                    messages.error(request, "Todo list already exists")
                else:
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

        # ✅ PREVENT DUPLICATE TODO ITEM
        if "item_title" in request.POST:
            title = request.POST.get("item_title").strip()

            if title:
                exists = TodoItem.objects.filter(
                    todo_list=todo_list,
                    title__iexact=title
                ).exists()

                if exists:
                    messages.error(request, "Task already exists")
                else:
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
                exists = TodoItem.objects.filter(
                    todo_list=todo_list,
                    title__iexact=new_title
                ).exclude(id=item_id).exists()

                if exists:
                    messages.error(request, "Task already exists")
                else:
                    TodoItem.objects.filter(
                        id=item_id,
                        todo_list=todo_list
                    ).update(title=new_title)

        return redirect("todo-detail", pk=pk)
