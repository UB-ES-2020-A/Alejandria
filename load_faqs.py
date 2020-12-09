import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Alejandria.settings")
django.setup()

from books.models import FAQ #  deepcode ignore C0413: <irrelevant error>

# pylint: disable=line-too-long

def read_faqs_from_file(): # pylint: disable=too-many-statements too-many-branches too-many-nested-blocks no-else-break
    """
    READS FAQs FROM A FILE:
    THE FILE FORMAT IS DEFFINED IN faqs.txt
    """
    # Using readlines()
    print("READING FILE...")
    filename = 'faqs.txt'
    file_faqs = open(filename, 'r')
    lines = file_faqs.readlines()
    print(lines)

    # Strips the newline character
    i = 0  # Line we are reading
    more_faqs = len(lines) > 0

    while more_faqs: # pylint: disable=too-many-nested-blocks

        cat = None
        q = list()
        a = list()
        first_q_line = True
        first_a_line = True
        line = lines[i]
        if "<cat>" in line and "</cat>" in line:
            print(line[5:-7])
            if line[5:-7] in [cat[0] for cat in FAQ.FAQ_CHOICES]:
                cat = line[5:-7]
                inprocess = True
                i += 1
            else:
                raise Exception("File format error")
            while inprocess:
                line = lines[i]
                if "<q>" in line:
                    # We found the question
                    q.append(line[3:])
                    while True:
                        if "</q>" in line:
                            # Ends the question
                            q.pop()
                            if first_q_line:
                                q.append(line[3:-5])
                            else:
                                q.append("<br>")
                                q.append(line[:-5])
                            break
                        # We are in a middle line
                        q.append("<br>")
                        q.append(line)
                        first_q_line = False
                        i += 1

                if "<a>" in line:
                    # Answer
                    # We found the question
                    while True:
                        line = lines[i]
                        if "</a>" in line:
                            # Ends the question
                            if first_a_line:
                                a.append(line[3:-5])
                            else:
                                a.append("<br>")
                                a.append(line[:-5])
                            save_faq(cat, q, a)
                            inprocess = False
                            more_faqs = len(lines) > i + 2
                            break
                        # We are in a middle line
                        if first_a_line:
                            a.append(line[3:-1])
                        else:
                            a.append("<br>")
                            a.append(line[:-1])
                        first_a_line = False
                        i += 1
                    i += 1
                i += 1
        else:
            i += 1
            print(i)

    print("ALL FAQS CREATED...OK")


def save_faq(cat, q, a):
    """
    Saves a faq passing
    Parameters:
        cat : category
        q: question
        a: answer
    """
    question = "".join(q)
    answer = "".join(a)
    new_faq = FAQ(question=question, answer=answer, category=cat)
    new_faq.save()
    print("FAQ SAVED: " + str(new_faq))

print("RF: Reaf file (faqs.txt)")
print("DB: Read whats in the database")
print("DEL: Delete whattever is in the database")
while True:
    what = input(" Choose (RF/DB/DEL), default(RF) : ")
    if what in 'RF' or what in '' or what in '\n': #pylint: disable=no-else-break
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
    else:
        print("Introduce a valid option")