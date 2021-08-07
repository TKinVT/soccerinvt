from flask import Flask, render_template, request
import requests
import posts, slack_funcs, image_search, slack_views
import json


app = Flask(__name__)


# BLOG GET ROUTES
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


# SLACK POST ROUTES
@app.route('/slack_action', methods=['POST'])
def slack_action():
    payload = json.loads(request.form['payload'])
    type = payload['type']

    if type == 'block_actions':
        action = payload['actions'][0]
        action_id = payload['actions'][0]['action_id']
        trigger_id = payload['trigger_id']
        print(action)
        if 'image_selection' in action_id:
            # import pprint
            # pprint.pprint(payload['actions'])
            view_id = payload['view']['id']
            # We use the block's action_id to encode the Post's id
            post_id = payload['actions'][0]['action_id'].split("|")[1]
            pic_url = payload['actions'][0]['value']
            posts.update_post(post_id, photo=pic_url)
            r = slack_funcs.confirm_submission(view_id)
            # r = requests.post(payload['response_url'], json={"delete_original": "true"})

        elif action_id == 'search_photos':
            view_id = payload['view']['id']
            post_id = payload['view']['private_metadata']
            values = payload['view']['state']['values']
            print(values)
            search_term = values['search_term']['search_photos']['value']
            # view = slack_funcs.update_modal_photo_search_results(search_term, post_id)
            r = slack_funcs.update_modal_photo_search_results(search_term, post_id, view_id)

    elif type == 'view_submission':
        callback_id = payload['view']['callback_id']
        values = payload['view']['state']['values']

        if callback_id == 'new_post':
            title = values['title']['text']['value']
            body = values['body']['text']['value']
            photo_url = values['photo_url']['text']['value']
            tags = values['tags']['text']['value']
            if tags:
                tags = [x.strip() for x in tags.split(",")]
            post_id = posts.new_post(body, title=title, photo=photo_url, tags=tags)
            post_id = str(post_id)

            if photo_url:
                return 'Got it :thumbsup:'
            else:
                view = slack_funcs.update_modal_photo_search(post_id)
                return {'response_action': 'update', 'view': view}

        # elif callback_id == 'search_photos':
        #     post_id = payload['view']['private_metadata']
        #     search_term = values['search_term']['text']['value']
        #     view = slack_funcs.update_modal_photo_search_results(search_term, post_id)
        #     return {'response_action': 'update', 'view': view}

        elif callback_id == 'search_results':
            post_id = payload['view']['private_metadata']
            view = slack_funcs.update_modal_photo_search(post_id)
            return {'response_action': 'update', 'view': view}

    return ""


@app.route('/slack', methods=['POST'])
def slack():
    r = request.form
    if r['user_id'] == "UG9RLD8FL":
        text = r['text']
        if len(text) < 1:
            return slack_funcs.open_modal(r['trigger_id'])
        else:
            post = slack_funcs.post_parser(text)
            posts.new_post(post['text'], tags=post['tags'])
            return "Got it :thumbsup:"
    else:
        return "Nuh uh uh"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
