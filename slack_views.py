new_post_view = {
    "type": "modal",
    "callback_id": "new_post",
    "submit": {
        "type": "plain_text",
        "text": "Submit",
        "emoji": True
    },
    "close": {
        "type": "plain_text",
        "text": "Cancel",
        "emoji": True
    },
    "title": {
        "type": "plain_text",
        "text": "New Post",
        "emoji": True
    },
    "blocks": [
        {
            "type": "input",
            "block_id": "title",
            "element": {
                "type": "plain_text_input",
                "action_id": "text"
            },
            "label": {
                "type": "plain_text",
                "text": "Title",
                "emoji": True
            },
            "optional": True
        },
        {
            "type": "input",
            "block_id": "body",
            "element": {
                "type": "plain_text_input",
                "multiline": True,
                "action_id": "text"
            },
            "label": {
                "type": "plain_text",
                "text": "Body",
                "emoji": True
            }
        },
        {
            "type": "input",
            "block_id": "photo_url",
            "element": {
                "type": "plain_text_input",
                "action_id": "text"
            },
            "label": {
                "type": "plain_text",
                "text": "Photo URL",
                "emoji": True
            },
            "optional": True
        },
        {
            "type": "input",
            "block_id": "tags",
            "element": {
                "type": "plain_text_input",
                "action_id": "text"
            },
            "label": {
                "type": "plain_text",
                "text": "Tags",
                "emoji": True
            },
            "optional": True,
            "hint": {
                "type": "plain_text",
                "text": "Comma separated list of tags, no need for hashtags"
            }
        }
    ]
}

photo_search_view = {
	"type": "modal",
    "callback_id": "search_photos",
    "private_metadata": None,
	"close": {
		"type": "plain_text",
		"text": "Cancel",
		"emoji": True
	},
	"title": {
		"type": "plain_text",
		"text": "Photo Search",
		"emoji": True
	},
	"blocks": [
		{
			"type": "input",
            "dispatch_action": True,
            "block_id": "search_term",
			"element": {
				"type": "plain_text_input",
				"action_id": "search_photos"
			},
			"label": {
				"type": "plain_text",
				"text": "Search Term",
				"emoji": True
			}
		}
	]
}

results_view_base =  {
	"type": "modal",
    "callback_id": "search_results",
    "private_metadata": None,
    "submit": {
		"type": "plain_text",
		"text": "New Search",
		"emoji": True
	},
	"close": {
		"type": "plain_text",
		"text": "Cancel",
		"emoji": True
	},
	"title": {
		"type": "plain_text",
		"text": "Photo Search",
		"emoji": True
	},
	"blocks": []
}

def make_photo_block(image_url):
    block_list = [{
        "type": "image",
        "image_url": image_url,
        "alt_text": "arsenal"
    },
    {
    "type": "actions",
    "elements": [{
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Use This One",
                "emoji": True
            },
            "value": image_url,
            "action_id": "image_selection"
        }]
    }]

    return block_list

divider_block = {
    "type": "divider"
}


confirmation_view = {
	"type": "modal",
	"close": {
		"type": "plain_text",
		"text": "Close",
		"emoji": True
	},
	"title": {
		"type": "plain_text",
		"text": "Submission confirmed",
		"emoji": True
	},
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Got it :thumbsup:",
				"emoji": True
			}
		}
	]
}
