from django.shortcuts import render
from core.models import Product


def home(request):
    context = {
                'products': Product.objects.all(),
    }
    return render(request, 'core/home.html', context)