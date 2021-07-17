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
