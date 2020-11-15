import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Alejandria.settings")
import django

django.setup()

from books.models import Book, User, Address, Product
import random

from books.models import FAQ


def write_some_faqs():
    while True:
        n = input("Number of faqs you whant to write:")
        if n.isdigit():
            n = int(n)
            break
        else:
            print("Introduce number")

    questions = list()
    answers = list()
    categories = list()

    for i in range(n):
        loop = True
        category = "DEFAULT"
        while loop:
            category = input("CATEGORY (DWLDBOOK, DEVOL, SELL, FACTU, CONTACT):")
            loop = False
        question = input("Question:")
        answer = input("Answer")

        categories.append(category)
        questions.append(question)
        answers.append(answer)

    faqs = list(zip(categories, questions, answers))
    print("Faqs:",faqs)
    create_faqs(faqs)


def read_faqs_from_file():
    # Using readlines()
    filename = 'faqs.txt'
    file1 = open(filename, 'r')
    lines = file1.readlines()

    questions = list()
    answers = list()
    categories = list()

    # Strips the newline character
    for line in lines:
        print(line)
        category, question, answer = line.strip().split('///')
        questions.append(question)
        answers.append(answer)
        categories.append(category)

    faqs = list(zip(categories, questions, answers))
    create_faqs(faqs)


def create_faqs(faqs):
    for faq in faqs:
        print("### FAQ ---->", faq)
        to_save = FAQ(question=faq[1], answer=faq[2], category=faq[0])
        print(to_save)
        to_save.save()


what = input("Chose option, insert manually, read in file information, see whats in database or delete all FAQ"
             " (I/RF/DB/DEL) :")
while True:
    if what == 'I':
        write_some_faqs()
        break
    elif what == 'RF':
        read_faqs_from_file()
        break
    elif what == 'DB':
        faqs = FAQ.objects.all()
        print(faqs)
        for faq in faqs:
            print(faq)
        break
    elif what == 'DEL':
        FAQ.objects.all().delete()
        print(FAQ.objects.all())
        break
