from django.views import generic 
from django.shortcuts import get_object_or_404,redirect
from .carts import Cart # Ensure correct filename: carts.py
from Product.models import Product

class AddToCart(generic.View):
    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')  # Use correct key
        product = get_object_or_404(Product, id=product_id)

        cart = Cart(request)  # Capital 'C' in Cart (class), lowercase 'request'
        cart.update(product_id=product.id, quantity=1)

        return redirect('product-details', slug=product.slug)


class CartItems(generic.TemplateView):
        template_name = 'cart/cart.html'
    

        def get(self, request, *args, **kwargs):
         product_id = request.GET.get('product_id',None)
         quantity = request.GET.get('quantity',None) 
         clear = request.GET.get('clear', False)  
         cart = Cart(request)
         if product_id and quantity :
           
            cart.update(int(product_id),int (quantity))
            return redirect('cart')
         if clear:
            cart.clear()
            return redirect('cart')


         return super().get(self,request, *args, **kwargs)
    
    