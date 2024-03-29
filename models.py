import os
from dotenv import load_dotenv
from mongoengine import *
from datetime import datetime

load_dotenv()

USERNAME = os.getenv("MONGODB_USERNAME")
PASSWORD = os.getenv("MONGODB_PASSWORD")
URL = os.getenv("MONGOATLAS_URL")

connect('tkinvt', host=f"mongodb+srv://{USERNAME}:{PASSWORD}@{URL}?retryWrites=true&w=majority")


class Post(Document):
    content = StringField(required=True)
    date = DateTimeField(default=datetime.utcnow, required=True)
    display_date = StringField(default=datetime.utcnow().strftime('%d/%b/%y'), required=True)
    photo = URLField()
    tags = ListField(StringField(max_length=90))
    title = StringField(max_length=90)

    meta = {
        'ordering': ['-date']
    }

    def __repr__(self):
        if self.title:
            return f"{self.id}|*{self.title}*"
        else:
            max = sorted([len(self.content), 20])[0]
            return f"{self.id}|{self.content[:max].rstrip()}"

    def add_tag(self, *tags):
        t = self.tags
        for tag in tags:
            t.append(tag)
        t.sort()
        self.save()

    def remove_tag(self, *tags):
        for tag in tags:
            self.update(pull__tags=tag)
        self.save()

    @classmethod
    def get_tags(cls):
        tags = cls.objects.distinct('tags')

        return tags

    @classmethod
    def tags_count(cls):
        tags_list = cls.get_tags()
        # https://docs.python.org/3/howto/sorting.html#sortinghowto
        count = {tag: cls.objects(tags=tag).count() for tag in tags_list}

        return count

    @classmethod
    def sorted_tags(cls):
        tags_list = cls.get_tags()
        sorted_tags_list = sorted(tags_list,
                                  key=cls.tags_count().__getitem__, reverse=True)

        return sorted_tags_list

    @classmethod
    def delete_last(cls):
        last = cls.objects[0]
        last.delete()
