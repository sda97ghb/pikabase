def story_id_from_url(story_url: str):
    return int(story_url.rsplit("_", 1)[-1])
