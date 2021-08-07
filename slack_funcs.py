import json
import re
import os
import requests
import image_search
import slack_views
from dotenv import load_dotenv

load_dotenv()


SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
VIEW_OPEN_URL = 'https://slack.com/api/views.open'
VIEW_PUSH_URL = 'https://slack.com/api/views.push'
VIEW_UPDATE_URL = 'https://slack.com/api/views.update'
HEADERS = {"Authorization": "Bearer {}".format(SLACK_BOT_TOKEN)}


def post_parser(text):
    # Deal with tags if they exist
    tags = None
    if "#" in text:
        split = text.split("#")
        text = split[0].strip()
        tags = [tag.strip() for tag in split[1:]]

    return {"text":text, "tags":tags}


def open_modal(trigger_id):
    view = slack_views.new_post_view
    json = {'trigger_id': trigger_id, 'view': view}
    r = requests.post(VIEW_OPEN_URL, headers=HEADERS, json=json)
    return ""


def confirm_submission(view_id):
    view = slack_views.confirmation_view
    json = {'view_id': view_id, 'view': view}
    r = requests.post(VIEW_UPDATE_URL, headers=HEADERS, json=json)


def update_modal_photo_search(post_id):
    view = slack_views.photo_search_view
    view['private_metadata'] = post_id
    return view


def update_modal_search_results(search_term, post_id, view_id):
    pics = image_search.image_search(search_term)
    view = slack_views.results_view_base
    view['private_metadata'] = post_id
    # I don't know why it happens, but slack carries over the results of previous
    # search_results, we clear that out
    view['blocks'] = []

    for pic in pics:
        view['blocks'].append(slack_views.divider_block)
        photo_block_elements = slack_views.make_photo_block(pic)
        for element in photo_block_elements:
            view['blocks'].append(element)

    json = {'view_id': view_id, 'view': view}
    requests.post(VIEW_UPDATE_URL, headers=HEADERS, json=json)
