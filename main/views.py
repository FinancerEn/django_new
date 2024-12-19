from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Product


def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 10)  # 10 продуктов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/product_list.html', {'page_obj': page_obj})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'main/product_detail.html', {'product': product})


def index(request):
    return render(request, 'main/index.html')
