from books.models import Author, UserDummy, Book, Product, Rating, Bill, FAQ, Cart


# TODO: Make test "en cadena". If we have to test something before try one test, do it.

def test_author():
    # Data to test
    first_name = 'Homero'
    last_name = 'Simpson'
    # Model creation
    obj = Author(first_name=first_name, last_name=last_name)
    obj.save()
    # Retrieve model to check correct creation
    obj = Author.objects.all().first()
    check = all([first_name == obj.first_name, last_name == obj.last_name])
    # Test sucess if check is True
    assert check


def test_book():
    # Data to test
    ISBN = '0123456789012'  # 13 digits
    user_id = UserDummy()
    title = 'THis is the TITLE'
    description = 'This is the description of a test book'
    saga = 'SAGA\'S NAME'
    authors = list(Author.objects.all()[:10])
    # publication_date = default
    price = 23.45
    language = 'Español'
    genre = 'Fantasy'
    publisher = 'Alejandria'
    num_pages = 100
    num_sold = 0
    recommended_age = 'Juvenile'
    thumbnail = '/thumbnails/1234567.png'

    obj = Book(ISBN=ISBN, user_id=user_id, title=title, description=description,
               saga=saga, authors=authors, price=price, language=language, genre=genre,
               publisher=publisher, num_pages=num_pages, num_sold=num_sold,
               recommended_age=recommended_age, thumbnail=thumbnail)
    obj.save()

    obj = Book.objects.filter(ISBN=ISBN)
    check = all([ISBN == obj.ISBN, user_id == obj.user_id, title == obj.title, description == obj.description,
                 saga == obj.saga, authors == obj.authors, price == obj.price, language == obj.language,
                 genre == obj.genre, publisher == obj.publisher, num_pages == obj.num_pages, num_sold == obj.num_sold,
                 recommended_age == obj.recommended_age, thumbnail == obj.thumbnail])

    # TODO: TEST EVERY POSSIBLE OUTCOME

    assert check


def test_product():
    ISBN = Book.objects.filter(ISBN='0123456789012')  # 13 digits
    price = 22.40
    fees = 21.00
    discount = 5.00

    obj = Product(ISBN=ISBN, price=price, fees=fees, discount=discount)
    obj.save()

    obj = Product.objects.all().first()
    check = all([ISBN == obj.ISBN, price == obj.price, fees == obj.fees, discount == obj.discount])

    assert check


def test_rating():
    product_id = Product.objects.all().first()
    user_id = UserDummy.objects.all().first()
    text = 'My opinion is that this product is great.'
    score = 3  # TODO: Also test if I use not viable scores
    # date = default

    obj = Rating(product_id=product_id, user_id=user_id, text=text, score=score)
    obj.save()

    obj = Product.objects.all().first()

    check = all([product_id == obj.product_id, user_id == obj.user_id,
                 text == obj.text, score == obj.score])
    assert check


def test_cart():
    ISBN1 = Book.objects.filter(ISBN='0123456789012')  # 13 digits
    price1 = 22.40
    fees1 = 21.00
    discount1 = 5.00
    prod_1 = Product(ISBN=ISBN1, price=price1, fees=fees1, discount=discount1)
    prod_1.save()

    ISBN2 = Book.objects.filter(ISBN='0123456789012')  # 13 digits
    price2 = 23.40
    fees2 = 0.00
    discount2 = 0.00
    prod_2 = Product(ISBN=ISBN2, price=price2, fees=fees2, discount=discount2)
    prod_2.save()

    products = Product.objects.all()[:3]

    obj = Cart(products=products)


def test_bill():
    ISBN1 = Book.objects.filter(ISBN='0123456789012')  # 13 digits
    price1 = 22.40
    fees1 = 21.00
    discount1 = 5.00
    prod_1 = Product(ISBN=ISBN1, price=price1, fees=fees1, discount=discount1)
    prod_1.save()

    ISBN2 = Book.objects.filter(ISBN='0123456789012')  # 13 digits
    price2 = 23.40
    fees2 = 0.00
    discount2 = 0.00
    prod_2 = Product(ISBN=ISBN2, price=price2, fees=fees2, discount=discount2)
    prod_2.save()

    cart = Cart(products=Product.objects.all()[:3])
    cart.save()
    cart = Cart.objects.all().first()

    user_id = UserDummy.objects.all().first()
    # date = default
    seller_info = ' This is the information of the Seller'
    payment_method = 'PayPal'

    obj = Bill(cart=cart, user_id=user_id,
               seller_info=seller_info, payment_method=payment_method)
    obj.save()

    obj = Bill.objects.all().first()

    check = all([cart == obj.cart, user_id == obj.user_id,
                 seller_info == obj.seller_info, payment_method == obj.payment_method])
    assert check


def test_faq():
    question = 'How is this Sprint going?'
    answer = 'Perfectly'

    obj = FAQ(question=question, answer=answer)
    obj.save()

    obj = FAQ.objects.all().first()

    check = all([question == obj.question, answer == obj.answer])

    assert check

