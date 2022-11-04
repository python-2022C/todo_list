from django.views import View
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.models import User
from .models import Task


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
        
        

