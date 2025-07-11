from django.conf import settings

from Product.models import Product

class Cart(object):
    def __init__(self, request)->None:
         self.session = request.session
         self.cart_id = settings.CART_ID 
         cart = self.session.get(self.cart_id)
         self.cart = self.session[self.cart_id] = cart if cart else {}

    def update (self,product_id , quantity=1 ):
         product = Product.objects.get(id=product_id)
         self.session[self.cart_id].setdefault(str(product_id),{'quantity':0})
         update_qantity =  self.session[self.cart_id][str (product_id)]['quantity'] + quantity
         self.session[self.cart_id][str (product_id)]['quantity']=  update_qantity
         self.session[self.cart_id][str (product_id)]['subtotal']=  update_qantity*float(product.price)
         if update_qantity < 1 :
              del self.session[self.cart_id][str(product_id)]
              self.save()

    def  __iter__(self):
         products = Product.objects.filter(id__in=list(self.cart.keys()))
         cart = self.cart.copy()

         for item in products:
              products = Product.objects.get(id=item.id)   
              cart [str(item.id)]['product'] ={
                   "id":item.id,
                   "tittle":item.tittle,
                   "Catagory":item.Catagory.tittle,
                   "price":float(item.price),
                   "thumbnail":item.thumbnail,
                   "slug":item.slug
              }
              yield cart[str(item.id)]


    def save(self):
         self.session.modified = True

    def __len__(self):
         return len(list(self.cart.keys()))     
     
    def clear(self):
        """Clears the cart"""
        del self.session[self.cart_id]
        self.session.modified = True

    def  restore_after_logout(self, cart={}):
        self.cart = self.session[self.cart_id] = cart 
        self.save()
    
    
    
    def  total(self):
        amount = sum(product['subtotal'] for product in self.cart.values())
        return amount