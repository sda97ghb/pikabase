import unittest

from pikabu.api.comments import story_comments
from pikabu.utils import story_id_from_url


class UtilsTests(unittest.TestCase):
    def test_story_id_from_url(self):
        story_id = story_id_from_url(
            "https://pikabu.ru/story/v_ssha_nabiraet_oborotyi_dvizhenie_kotoryie_vyismeivaet_novuyu_gollivudskuyu_modu_snimat_v_roli_belyikh_istoricheskikh_personazhey_chernokozhikh_aktyorov_8034385"
        )
        self.assertEqual(story_id, 8034385)


class CommentsTests(unittest.TestCase):
    def test_story_comments(self):
        comments = story_comments(
            "https://pikabu.ru/story/v_ssha_nabiraet_oborotyi_dvizhenie_kotoryie_vyismeivaet_novuyu_gollivudskuyu_modu_snimat_v_roli_belyikh_istoricheskikh_personazhey_chernokozhikh_aktyorov_8034385"
        )
        # Result has at least few comments
        next(comments)
        next(comments)
        next(comments)
