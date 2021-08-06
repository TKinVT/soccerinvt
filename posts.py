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
    display_date =StringField(default=datetime.utcnow().strftime('%d/%b/%y'), required=True)
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


#############################
#
# GET-type Functions
#
#############################

def get_posts():
    posts = Post.objects

    return posts


def get_tagged_posts(tag):
    tagged_posts = Post.objects(tags=tag)

    return tagged_posts

def get_long_posts():
    # Not really implemented yet

    return []


def get_tags():
    tags = Post.objects.distinct('tags')

    return tags


def tags_count():
    tags_list = get_tags()
    # https://docs.python.org/3/howto/sorting.html#sortinghowto
    count = {tag:Post.objects(tags=tag).count() for tag in tags_list}

    return count


def sorted_tags():
    tags_list = get_tags()
    sorted_tags_list = sorted(tags_list,
                              key=tags_count().__getitem__, reverse=True)

    return sorted_tags_list


def header_tags():
    tags_list = sorted_tags()

    return tags_list[:5]


#############################
#
# POST & PUT-type Functions
#
#############################

def new_post(content, photo=None, tags=None, title=None):
    if tags:
        print(tags)
        tags.sort()
        print(tags)
    p = Post(content=content, photo=photo, tags=tags, title=title)
    p.save()
    return p.id


def update_post(id, **items):
    p = Post.objects.get(id=id)
    for item in items:
        print(f"{item}: {items[item]}")
        p.__setattr__(item, items[item])
    p.save()


def add_tag(id, *tags):
    p = Post.objects.get(id=id)
    # for tag in tags:
    #     p.update(push__tags=tag)
    t = p.tags
    for tag in tags:
        t.append(tag)
    t.sort()
    p.save()


#############################
#
# DELETE-type Functions
#
#############################

def delete_last_post():
    p = Post.objects[0]
    p.delete()


def delete_post(id):
    p = Post.objects.get(id=id)
    p.delete()


def remove_attribute(id, *items):
    p = Post.objects.get(id=id)
    for item in items:
        p.__setattr__(item, None)
    p.save()


def remove_tag(id, *tags):
    p = Post.objects.get(id=id)
    for tag in tags:
        p.update(pull__tags=tag)


if __name__ == '__main__':
    pass
