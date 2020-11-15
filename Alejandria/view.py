from django.shortcuts import render


def home(request):
    template = "home.html"
    context = {}

    return render(request, template, context)


def search0(request):
    template = "searchresult.html"
    # book0 = Book(title="Song of Ice and Fire", author="George R. R. Martin", price=24.95)
    # book1 = Book(title="The Mist", author="Stephen King", price=19.99)
    # coincidents = [book0, book1]
    context = {"coincidents": coincidents}

    return render(request, template, context)


def showDetails(request, isbn):
    template = "details.html"
    context = {"isbn": isbn}

    return render(request, template, context)


def search(request):
    template = "search.html"
    context = {}

    return render(request, template, context)


def cart(request):
    template = "cart.html"
    context = {}

    return render(request, template, context)


def payment(request):
    template = "payment.html"
    context = {}

    return render(request, template, context)


def delete_product(request, product_id):
    template = "delete_product.html"
    context = {product_id}
    return render(request, template, context)
