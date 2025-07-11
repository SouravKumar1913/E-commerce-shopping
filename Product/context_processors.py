from .models import Catagory

def categories(request):
    return {"categories": Catagory.objects.all()}