new_post_view = {
    "type": "modal",
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
