import os

import requests.adapters

session = requests.Session()
session.mount(
    "https://pikabu.ru/", requests.adapters.HTTPAdapter(pool_maxsize=os.cpu_count())
)
session.headers.update(
    {
        "Origin": "https://pikabu.ru",
        "Host": "pikabu.ru",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0",
    }
)


def get_story_comments(story_id, min_comment_id=None, exclude_ids=None):
    fields = {
        "action": "get_story_comments",
        "story_id": story_id,
    }
    if min_comment_id:
        fields["min_comment_id"] = min_comment_id
    if exclude_ids:
        fields["exclude_ids"] = ",".join(map(str, exclude_ids))

    response = session.post("https://pikabu.ru/ajax/comments_actions.php", data=fields)
    response.raise_for_status()
    return response.json()
