import uuid 
import json
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from Product.models import Product
from cart.carts import Cart
from .models import Order,OrderItem

from .forms import CheckoutForm



class Checkout(LoginRequiredMixin,generic.View):
    login_url = reverse_lazy('login') 
    def get(self, *args, **kwargs):
       
        form = CheckoutForm()      
        context = {
            'form':form
        }
        return render(self.request , 'order/checkout.html', context)
    

    def post(self , *args, **kwargs):
        form = CheckoutForm(self.request.POST)

        if form.is_valid():
            data = form.changed_data
            print(data)
            return JsonResponse({
               'success': True,
               "errors": None
            })
        else:
            return JsonResponse({
               'success': False,
               "errors": dict(form.errors)
            })
        
class SaveOrder(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('login')

    def post(self, *args, **kwargs):
        try:
            customer_information = json.loads(self.request.body)
            cart = Cart(self.request)
            user_cart = cart.cart  # Using cart object directly

            # Check if there are any products in the cart
            if not user_cart:
                return JsonResponse({'error': 'No products in cart'}, status=400)

            # Get the products in the cart
            product_ids = list(user_cart.keys())
            products = Product.objects.filter(id__in=product_ids)

            ordered_products = []

            # Create order items and add them to the order
            for item in cart:
             order_item = OrderItem.objects.create(
             product_id=item['product']['id'],
             price=item['product']['price'],
             quantity=item['quantity']
            )
            ordered_products.append(order_item)

             # Create the order
            order = Order.objects.create(
              user=self.request.user,
              transaction_id=uuid.uuid4().hex,
              **customer_information
            )

             # Link the order items
            order.order_items.add(*ordered_products)
       

            # Check if the total amount matches
            if  float('%.2f' % cart.total()) != float(order.total):

                order.paid = False
            else:
                order.paid = True

            order.save()

            # Clear the cart after saving the order
            cart.clear()

            # Return success response
            return JsonResponse({'success': True})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500) 



class Orders(LoginRequiredMixin,generic.ListView):
    lohin_url = reverse_lazy('login')
    model = Order 
    template_name= 'order/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)