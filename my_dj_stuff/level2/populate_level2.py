import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'level2.settings')

import django
django.setup()

#Fake POP script
import random
from level2app.models import AccessRecord, Webpage, Topic
from faker import Faker

fakgen = Faker()
topics = ['Search', 'Social', 'News']

def add_topic():
    # get_or_create creates a tuple
    t = Topic.objects.get_or_create(top_name=random.choice(topics))[0]
    t.save()
    return t

def populate(n=5):
    for entry in range(n):
        # get topic
        top = add_topic()

        # create fake data
        fake_url = fakgen.url()
        fake_date = fakgen.date()
        fake_name = fakgen.name()

        # create the new webpage entry
        webpg = Webpage.objects.get_or_create(topic=top, url=fake_url, name=fake_name)[0]
        # create fake AccessRecord
        acc_rec = AccessRecord.objects.get_or_create(name=webpg, date=fake_date)[0]

if __name__ == '__main__':
    print('start population')
    populate(10)
    print('population complete!')