import re


def post_parser(text):
    # Deal with title if it exists
    title_re = "!!.+!!"
    title = re.search(title_re, text)
    if title:
        # If title exists, strip away exclamation points
        title = title.group()[2:-2]
        # Remove title, and whitespace, from text
        text = re.sub(title_re, "", text).strip()

    # Deal with tags if they exist
    tags = None
    if "#" in text:
        split = text.split("#")
        text = split[0].strip()
        tags = [tag.strip() for tag in split[1:]]

    return {"text":text, "title":title, "tags":tags}


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
