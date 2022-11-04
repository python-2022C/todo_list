from django.views import View
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.models import User



def user_convert_to_duct(customer: User) -> dict:
    return {
        'id': customer.id,
        'username': customer.username,
        'firstname': customer.first_name,
        'lastname': customer.last_name,
        'email': customer.email,
        'date_joined': customer.date_joined,
        'is_active': customer.is_active,
        'last_login': customer.last_login
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
