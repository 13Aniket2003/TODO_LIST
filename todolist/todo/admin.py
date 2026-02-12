from django.contrib import admin
from .models import LoginUser,SignupUser,TodoList, TodoItem

admin.site.register(LoginUser)
admin.site.register(SignupUser)
admin.site.register(TodoList)
admin.site.register(TodoItem)
