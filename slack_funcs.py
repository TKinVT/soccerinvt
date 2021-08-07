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


def pic_choice(pics, post_id):
    slack_blocks = {"blocks" : []}
    blocks = slack_blocks["blocks"]

    header = [
        {
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Choose an image for your post",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "This is a plain text section block.",
				"emoji": True
			}
		}
    ]

    for element in header:
        blocks.append(element)

    for pic in pics:
        pic_block_elements = [
            {
    			"type": "divider"
    		},
            {
    			"type": "image",
    			"image_url": pic,
    			"alt_text": "arsenal"
    		},
            {
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Use This One",
						"emoji": True
					},
					"value": pic,
					"action_id": f"image_selection|{post_id}"
				}
			  ]
		    }
        ]
        for element in pic_block_elements:
            blocks.append(element)

    footer = [
        {
		"type": "divider"
	},
	{
		"type": "divider"
	},
	{
		"type": "actions",
		"elements": [
			{
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "CANCEL",
					"emoji": True
				},
				"style": "danger",
				"value": "cancel",
				"action_id": "cancel"
			}
		]
	}
    ]

    for element in footer:
        blocks.append(element)

    return slack_blocks


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
    view = slack_views.photos_view
    view['private_metadata'] = post_id
    return view


def make_results_base(post_id):
    view = slack_views.results_view_base
    print(view['blocks'])
    view['private_metadata'] = post_id
    # I don't know why it happens, but slack carries over the results of previous
    # search_results, we clear that out
    view['blocks'] = []
    return view

def update_modal_photo_search_results(search_term, post_id, view_id):
    pics = image_search.image_search(search_term)
    base_view = make_results_base(post_id)
    blocks_to_add = []

    for pic in pics:
        pic_block_elements = []
        pic_block_elements.append(slack_views.photo_block_elements[0])
        pic_block_elements.append({
            "type": "image",
            "image_url": pic,
            "alt_text": "arsenal"
        })
        pic_block_elements.append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Use This One",
                        "emoji": True
                    },
                    "value": pic,
                    "action_id": f"image_selection|{post_id}"
                }
              ]
        })
        # x =
        # y =
        #
        # pic_block_elements.append(x)
        # pic_block_elements.append(y)

        for element in pic_block_elements:
            base_view['blocks'].append(element)

    # import pprint
    # pprint.pprint(blocks_to_add)

    # for block in blocks_to_add:
    #     base_view['blocks'].append(block)

    # return base_view
    json = {'view_id': view_id, 'view': base_view}
    requests.post(VIEW_UPDATE_URL, headers=HEADERS, json=json)
