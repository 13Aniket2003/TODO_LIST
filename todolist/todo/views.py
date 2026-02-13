from django.template import loader
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import LoginUser,SignupUser,TodoList, TodoItem


from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 1. Create the user
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # 2. Send the Welcome Email
            subject = "Welcome to Our Website!"
            message = f"Hi {username}, thanks for signing up. We're glad to have you!"
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email], # Send to the email the user just typed in
                    fail_silently=False,
                )
            except Exception as e:
                # Log the error but don't stop the user from signing up
                print(f"Mail error: {e}")

            messages.success(request, "Account created! Check your email.")
            return redirect('login') 

    return render(request, "signup.html")


from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # This checks the built-in User model and verifies the hashed password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) # Creates the session
            
            # --- Send Login Email ---
            try:
                send_mail(
                    "New Login Alert",
                    f"Hi {user.username}, you just logged in to your account.",
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Login mail error: {e}")
            # ------------------------

            messages.success(request, f"Welcome, {username}")
            return redirect("home")
        else:
            # If authenticate returns None, the credentials were wrong
            messages.error(request, "Invalid username or password")
        
    return render(request, "login.html")


from django.shortcuts import render, redirect
from django.views import View
from .models import TodoList


class HomeView(View):

    def get(self, request):
        lists = TodoList.objects.all()
        edit_list_id = request.GET.get("edit")  # for update mode

        return render(
            request,
            'home.html',
            {
                'lists': lists,
                'edit_list_id': edit_list_id
            }
        )

    def post(self, request):

        # ADD TODO LIST
        if 'list_name' in request.POST:
            list_name = request.POST.get('list_name', '').strip()

            if list_name and not TodoList.objects.filter(name__iexact=list_name).exists():
                TodoList.objects.create(name=list_name)

        # DELETE TODO LIST
        elif 'delete_list' in request.POST:
            TodoList.objects.filter(
                id=request.POST.get('delete_list')
            ).delete()

        # UPDATE TODO LIST (SAVE)
        elif 'update_list' in request.POST:
            list_id = request.POST.get('update_list')
            new_name = request.POST.get('new_name', '').strip()

            if new_name:
                TodoList.objects.filter(id=list_id).update(name=new_name)

        return redirect('home')



    
class TodoDetailView(View):

    def get(self, request, pk):
        todo_list = get_object_or_404(TodoList, id=pk)
        edit_item_id = request.GET.get('edit')

        return render(request,'todo_detail.html',{'list': todo_list,'edit_item_id': edit_item_id})

    def post(self, request, pk):
        todo_list = get_object_or_404(TodoList, id=pk)

        # ADD TODO ITEM
        if 'item_title' in request.POST:
            title = request.POST.get('item_title', '').strip()

            if title and not TodoItem.objects.filter(todo_list=todo_list,title__iexact=title).exists():
                TodoItem.objects.create(title=title,todo_list=todo_list)

        # DELETE TODO ITEM
        elif 'delete_item' in request.POST:
            TodoItem.objects.filter(id=request.POST.get('delete_item')).delete()

        # UPDATE TODO ITEM
        elif 'update_item' in request.POST:
            item_id = request.POST.get('update_item')
            new_title = request.POST.get('new_title', '').strip()

            if new_title and not TodoItem.objects.filter(todo_list=todo_list,title__iexact=new_title).exclude(id=item_id).exists():
                TodoItem.objects.filter(id=item_id).update(title=new_title)

        return redirect('todo-detail', pk=pk)
