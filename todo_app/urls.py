from django.urls import path
from .views import (
    GetCustomersView,
)


urlpatterns = [
    path(route='users/', view=GetCustomersView.as_view(), name='all_users'),
]
