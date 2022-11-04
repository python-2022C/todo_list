from django.views import View
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.models import User
from .models import Task
from datetime import datetime


def user_convert_to_duct(customer: User) -> dict:
    tasks = Task.objects.filter(customer=customer).count()
    return {
        'id': customer.id,
        'username': customer.username,
        'first_name': customer.first_name,
        'last_name': customer.last_name,
        'email': customer.email,
        'date_joined': customer.date_joined,
        'is_active': customer.is_active,
        'last_login': customer.last_login,
        'tasks': tasks,
    }



def task_convert_to_dict(task: Task) -> dict:
    print(task.customer)
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'is_completed': task.is_completed,
        'created_at': task.created_at,
        'updated_at': task.updated_at,
        'deatline': task.deatline,
        'importance': task.importance,
        'customer': user_convert_to_duct(User.objects.get(username=task.customer)) 
    }




class GetCustomersView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        customers = User.objects.all()
        customers_list = []
        for customer in customers:
            if customer.is_superuser or customer.is_staff:
                continue
            customers_list.append(user_convert_to_duct(customer))

        return JsonResponse({'users': customers_list})


class AddCustomerView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        data = request.POST
        print(User.objects.filter(username=data.get('username')).all())
        if not data.get('username'):
            return JsonResponse({'status': 'username is invalid'})
        elif not data.get('password'):
            return JsonResponse({'status': 'password is requirement'})
        elif User.objects.filter(username=data.get('username')).all():
            return JsonResponse({'status': 'User is already registred!'})
        elif data.get('is_staff', False):
            return JsonResponse({'status': 'don\'t access to staff'})
        elif data.get('is_superuser', False):
            return JsonResponse({'status': 'don\'t access to superuser'})
        
        customer = User()
        customer.username = data['username']
        customer.password = data['password']
        if data.get('first_name'):
            customer.first_name = data['first_name']
        if data.get('last_name'):
            customer.last_name = data['last_name']
        if data.get('email'):
            customer.email = data['email']
        customer.save()

        return JsonResponse({'user': user_convert_to_duct(customer)})
        
        
class CreateTaskView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        data = request.POST
        if not data.get('title'):
            return JsonResponse({'status': 'title is required'})
        elif not data.get('deatline'):
            return JsonResponse({'status': 'deatline is required'})
        elif not (data.get('username') or data.get('id')):
            return JsonResponse({'status': 'need username or id'})
        elif data.get('username'):  
            customer = User.objects.get(username=data['username'])
        elif data.get('id'):  
            customer = User.objects.get(id=int(data['id']))

        task = Task(
            title = data['title'],
            description = data.get('description', ''),
            deatline = datetime.strptime(data['deatline'], '%Y-%m-%d %H:%M'),
            importance = data.get('importance', 0),
            customer = customer
        )
        task.save()
        return JsonResponse({'task': task_convert_to_dict(task)})

