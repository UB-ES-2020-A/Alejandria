from django.shortcuts import render

def home(request):
    template = "home.html"
    context = {}

    return render(request, template, context)

def cart(request):
    template = "navbar.html"
    context = {}

    return render(request, template, context)
