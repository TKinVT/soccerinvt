from flask import Flask, render_template, request
import requests
import posts
import slack_funcs


app = Flask(__name__)


@app.route('/slack', methods=['POST'])
def slack():
    r = request.form
    if r['user_id'] == "UG9RLD8FL":
        text = r['text']
        post = slack_funcs.post_parser(text)
        posts.new_post(post['text'], title=post['title'], tags=post['tags'])
        return ""
    else:
        return "Nuh uh uh"

@app.route('/longer')
def longer():
    long_posts = posts.get_long_posts()
    return render_template('longer.html', posts=long_posts, tags=posts.header_tags())


@app.route('/tags')
def tags():
    count = posts.tags_count()
    counted = posts.sorted_tags()
    alpha = posts.get_tags()
    return render_template('tags.html', counted=counted, alpha=alpha,
                           tags=posts.header_tags(), count=count)


@app.route('/tag/<tag>')
def tagged_posts(tag):
    posts_ = posts.get_tagged_posts(tag)
    return render_template('tagged.html', posts=posts_, tag=tag, tags=posts.header_tags())


@app.route('/about')
def about():
    return render_template('about.html', tags=posts.header_tags())


@app.route('/')
def index():
        return render_template('index.html', posts=posts.get_posts(), tags=posts.header_tags())


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
