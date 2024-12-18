from django.shortcuts import render
from .models import Product, Category


def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'message': 'Добро пожаловать на главную страницу!',
        'products': products,
        'categories': categories
    }
    return render(request, 'index.html', context)
