import datetime
import json
import logging
from dataclasses import dataclass
from typing import Generator

from bs4 import BeautifulSoup

from pikabu.api.adapters import get_story_comments
from pikabu.utils import story_id_from_url

log = logging.getLogger(__name__)


@dataclass
class Comment:
    id: int
    parent_id: int
    username: str
    text: str
    date: datetime.datetime
    rating: int


class CommentJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Comment):
            return {
                "id": o.id,
                "parent_id": o.parent_id,
                "username": o.username,
                "text": o.text,
                "data": o.date.isoformat(),
                "rating": o.rating,
            }
        return super().default(o)


def story_comments(story_url: str) -> Generator[Comment, None, None]:
    story_id = story_id_from_url(story_url)

    min_comment_id = None
    exclude_ids = []

    while True:
        comments_response = get_story_comments(story_id, min_comment_id, exclude_ids)
        if "data" not in comments_response:
            log.warning("Malformed get_story_comments response: has no data")
            break
        if "comments" not in comments_response["data"]:
            log.warning("Malformed get_story_comments response: has no data.comments")
            break
        if not comments_response["data"]["comments"]:
            break  # all comments are read

        found_ids = []
        for comment in parse_comments(comments_response["data"]["comments"]):
            found_ids.append(comment.id)
            yield comment
        if min_comment_id is None:
            min_comment_id = min(found_ids)
        exclude_ids.extend(id_ - min_comment_id for id_ in found_ids)


def parse_comments(portion):
    for chunk in portion:
        chunk["html"] = BeautifulSoup(chunk["html"], features="html.parser")
        for comment in chunk["html"].find_all(class_="comment"):
            comment_id = extract_comment_id(comment)
            comment_body = comment.find(class_="comment__body", recursive=False)
            comment_header = comment_body.find(class_="comment__header")
            comment_text = comment_body.find(class_="comment__content").text.strip()
            comment_username = comment_header.find(class_="user__nick").text.strip()
            comment_date = datetime.datetime.fromisoformat(
                comment_header.find(class_="comment__datetime").attrs["datetime"]
            )
            try:
                comment_rating = int(
                    comment_header.find(class_="comment__rating-count").text.strip()
                )
            except:
                comment_rating = 0
            comment_parent = comment.find_parent(class_="comment")
            comment_parent_id = (
                extract_comment_id(comment_parent)
                if comment_parent is not None
                else None
            )
            yield Comment(
                id=comment_id,
                text=comment_text,
                username=comment_username,
                date=comment_date,
                rating=comment_rating,
                parent_id=comment_parent_id,
            )


def extract_comment_id(comment_tag):
    return int(comment_tag.attrs["id"][len("comment_") :])


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("story_url")
    parser.add_argument("--format", choices=["repr", "text", "json"], default="repr")
    args = parser.parse_args()

    comments = story_comments(args.story_url)

    if args.format == "repr":
        for n, comment in enumerate(comments, 1):
            print(f"{n}: {comment}")
    elif args.format == "text":
        for n, comment in enumerate(comments, 1):
            print(comment.text)
    elif args.format == "json":
        print(json.dumps(list(comments), cls=CommentJSONEncoder))


if __name__ == "__main__":
    main()
