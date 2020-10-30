from django.shortcuts import render


def cart(request):
    template = "navbar.html"
    context = {}

    return render(request, template, context)
