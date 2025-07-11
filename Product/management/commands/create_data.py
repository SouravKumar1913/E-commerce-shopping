import requests
from django.utils.text import slugify
from django.core.management.base import BaseCommand

from Product.models import Catagory, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Creating data from Fake Store API...')
        response = requests.get('https://fakestoreapi.com/products').json()

        for product in response:
            catagory, _ = Catagory.objects.get_or_create(
                tittle=product['category'],
                slug=slugify(product['category']),
                featured=True
            )
            Product.objects.create(
                Catagory=catagory,  # ✅ Match model field name exactly
                tittle=product['title'],  # ✅ Ensure JSON key is correct
                slug=slugify(product['title']),
                price=product['price'],  # ✅ Match model field name
                thumbnail=product['image'],  # API uses "image" not "thumbnail"
                description=product['description'],
            )

        print('✔ Insertion complete!')
