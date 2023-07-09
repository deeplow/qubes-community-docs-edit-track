"https://forum.qubes-os.org/t/guide-xfce-global-dark-mode-in-qubes-4-0-4-1/10757.json"
# curl  | jq ".post_stream.posts[0].cooked"

import json
import requests
import logging
import os
from glob import glob
from pathlib import Path
import re

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

DOCS_DIR = "docs"  # Stored in "docs/"
DOCS_CATEGORY_ID = 14
FORUM_DOMAIN = "https://forum.qubes-os.org"


def discourse_get_topic(topic_id: str):
    url_topic = f"{FORUM_DOMAIN}/t/{topic_id}.json"
    logging.info(f"Fetching {url_topic}")
    r = requests.get(url_topic)
    return json.loads(r.content)

def update_guide(topic_id: str):
    """Updates the local file for a certain guide"""

    ##
    # Get guide metadata
    ##
    topic_json = discourse_get_topic(topic_id)

    # Get the topic's dash-separated-title (to later use as the filename)
    topic_slug = topic_json["post_stream"]["posts"][0]["topic_slug"]

    ##
    # Get the markdown of the guide
    ##
    logging.info(f"Fetching markdown content for first post")
    url_topic_raw = f"{FORUM_DOMAIN}/raw/{topic_id}/1"
    r = requests.get(url_topic_raw)
    markdown = r.content

    ##
    # Update files
    ##

    # Slug will remain the same dispite renames
    guide_path_base = f"{DOCS_DIR}/{topic_id}-"
    new_guide_path = f"{guide_path_base}{topic_slug}.md"
    old_guide_path_glob = glob(f"{guide_path_base}*")
    if len(old_guide_path_glob) == 1:  # If found previous guide name
        old_guide_path   = old_guide_path_glob[0]
        is_guide_renamed = old_guide_path != new_guide_path
        is_new_guide     = True
    else:  # If is new guide
        old_guide_path   = None
        is_guide_renamed = False
        is_new_guide     = True

    logging.debug(
        f"\nGuide {topic_slug}:\n"
        f"\tNew guide? {is_new_guide}\n"
        f"\tRenamed?   {is_guide_renamed}\n"
    )

    # Save the new version of the guide
    logging.info(f"Updating new guide at '{new_guide_path}'")
    with open(new_guide_path, "w") as f:
        f.write(markdown.decode())

    # Remove old path
    if is_guide_renamed:
        os.remove(old_guide_path)
        # TODO git rename

    # TODO Update the docs index
    if is_new_guide:
        pass
    else:
        # does the title change
        pass

def get_subcategory_ids(parent_category_id: int):
    """Returns the subcategory IDs and the parent's ID"""
    api_endpoint = f"{FORUM_DOMAIN}/categories.json"
    logging.info(f"Fetching {api_endpoint}")
    r = requests.get(api_endpoint)
    json_data = json.loads(r.content)
    for category in json_data["category_list"]["categories"]:
        if category["id"] != parent_category_id:
            continue
        return [parent_category_id] + category["subcategory_ids"]

def update_guides(initialize=False):
    """Gets the latest version of guides"""
    if initialize:
        page_range = range(0,99)
    else:
        page_range = [0]

    # Explore guides category and respective subcategories
    for category_id in get_subcategory_ids(DOCS_CATEGORY_ID):
        logging.debug(f"Now looking at category {category_id}\n\n")
        for page in page_range:
            r = requests.get(f"{FORUM_DOMAIN}/c/guides/{category_id}/l/latest.json?page={page}")
            latest = json.loads(r.content)
            for topic in latest["topic_list"]["topics"]:
                topic_id = topic["id"]
                update_guide(topic_id)

def remove_old_guides():
    """
    Remove guides moved out of the category
    sometimes users post in the guides category mistakenly
    """
    for file in glob(f"{DOCS_DIR}/*.md"):
        basename = os.path.basename(file)
        topic_id = re.findall(r"\d+", basename)[0]
        topic_json = discourse_get_topic(topic_id)
        category_id = topic_json["category_id"]
        if category_id not in get_subcategory_ids(DOCS_CATEGORY_ID):
            logging.info(f"Found a misplaced non-guide... removing '{file}'")
            os.remove(file)

if __name__ == '__main__':
    update_guides(initialize=True)
    remove_old_guides()
