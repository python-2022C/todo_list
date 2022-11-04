from django.contrib import admin
from .models import Task


todo_app_models = [Task]
admin.site.register(todo_app_models)
