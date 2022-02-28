from flask import Flask, render_template, request

from models import Post

app = Flask(__name__)


@app.route('/')
def index():
    posts = Post.objects()
    header_tags = Post.sorted_tags()[:5]
    return render_template('index.html', posts=posts, tags=header_tags)


@app.route('/about')
def about():
    header_tags = Post.sorted_tags()[:5]
    return render_template('about.html', tags=header_tags)


@app.route('/tags')
def tags():
    count = Post.tags_count()
    counted = Post.sorted_tags()
    alpha = Post.get_tags()
    header_tags = Post.sorted_tags()[:5]
    return render_template('tags.html', counted=counted, alpha=alpha,
                           tags=header_tags, count=count)


@app.route('/tags/<tag>')
def tagged_posts(tag):
    posts_ = Post.objects(tags=tag).all()
    header_tags = Post.sorted_tags()[:5]
    return render_template('tagged.html', posts=posts_, tag=tag, tags=header_tags)


@app.route('/longer')
def longer():
    long_posts = Post.objects()
    header_tags = Post.sorted_tags()[:5]
    return render_template('longer.html', posts=long_posts, tags=header_tags)


@app.route('/new', methods=['POST'])
def new_post():
    data = request.json
    print(data)
    post = Post(content=data['content'])

    if 'title' in data and data['title'] is not None:
        post.title = data['title']

    if 'photo' in data and data['photo'] is not None:
        post.photo = data['photo']

    if 'tags' in data and data['tags'] is not None:
        post.tags = data['tags']

    post.save()

    return ""


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
