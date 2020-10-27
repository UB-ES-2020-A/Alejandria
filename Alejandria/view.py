from django.shortcuts import render


def cart(request):
    template = "cart.html"
    context = {}

    return render(request, template, context)
