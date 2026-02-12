from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password,identify_hasher


class LoginUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password:str)->None:
        """Hash and set a raw password"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password:str)->bool:
        return check_password(raw_password, self.password)    
    
    def save(self, *args, **kwargs):
        # ensure stored password is always hashed once
        try:
            identify_hasher(self.password)
        except ValueError:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)     

    def __str__(self):
        return self.username
    


class SignupUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password: str) -> None:
        self.password = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password(raw_password, self.password)
    
    def save(self, *args, **kwargs):
        try:
            identify_hasher(self.password)
        except ValueError:
            self.password = make_password(self.password)

        super().save(*args, **kwargs)


        login_user, _ = LoginUser.objects.get_or_create(username = self.username)
        login_user.password = self.password
        login_user.is_active = self.is_active
        login_user.save()

    def __str__(self):
        return self.username
    


class TodoList(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TodoItem(models.Model):
    todo_list = models.ForeignKey(TodoList,on_delete=models.CASCADE,related_name='items')
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
