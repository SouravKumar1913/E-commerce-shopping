from django.db.models import Q
from django.views import generic
from django.shortcuts import render
from django.core.paginator import (
    PageNotAnInteger,
    EmptyPage,
    InvalidPage,
    Paginator
)
from cart.carts import Cart 
from .models import (
    Catagory,
    Slider,
    Product,
)

class Home(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update (
            {
                'featured_categories':Catagory.objects.filter(featured=True),
                'featured_products':Product.objects.filter(featured=True),
                'sliders':Slider.objects.filter(show=True),
            }
        )
        return context 
class ProductDetails(generic.DetailView):
    model = Product
    template_name = 'product/product-details.html'
    slug_url_kwarg = 'slug'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = self.get_object().related
        return context 
    
class CategoryDetails(generic.DetailView):
    model = Catagory
    template_name = 'product/category-details.html'
    slug_url_kwarg = 'slug'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.get_object().products.all()
        return context    
    

class CustomPaginator:
    def __init__(self,request,queryset,paginted_by)->None:
         self.paginator = Paginator(queryset,paginted_by)
         self.paginated_by = paginted_by 
         self.queryset = queryset
         self.page = request.GET.get('page', 1)

    def get_queryset(self):
        try:
             querset = self.paginator.page(self.page) 
        except PageNotAnInteger:
            querset = self.paginator.page(1) 
        except EmptyPage:
              querset = self.paginator.page(1) 
        except InvalidPage:
              querset = self.paginator.page(1)

        return querset          
      
class ProductList(generic.ListView):
    model = Product
    template_name = 'product/product-list.html'
    context_object_name = 'object_list'
    paginate_by = 8

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       page_obj = CustomPaginator(self.request,self.get_queryset(),self.paginate_by )
       quryset = page_obj.get_queryset() 
       paginator = page_obj.paginator
       context['object-list'] = quryset
       context['paginator'] = paginator 
       return context 
  



class SearchProducts(generic.View):

    def get(self, request, *args, **kwargs):
        key = request.GET.get('key', '')

        products = Product.objects.filter(
            Q(tittle__icontains=key) |
            Q(Catagory__tittle__icontains=key)
        )

        context = {
            'products': products,
            'key': key
        }
        return render(request, 'product/search-products.html', context)
     
        
     
          