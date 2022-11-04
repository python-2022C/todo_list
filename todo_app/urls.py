from django.urls import path
from .views import (
    GetCustomersView,
    AddCustomerView,
    CreateTaskView
)


urlpatterns = [
    path(route='users/', view=GetCustomersView.as_view(), name='all_users'),
    path(route='register/', view=AddCustomerView.as_view(), name='register'),
    path(route='addtask/', view=CreateTaskView.as_view(), name='create_task'),
]
