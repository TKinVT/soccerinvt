from flask import Flask, render_template

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


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
