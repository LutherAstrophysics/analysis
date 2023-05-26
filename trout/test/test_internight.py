import random
import unittest

from trout.internight import _SPECIAL_STARS, InternightBands, get_band
from trout.stars.utils import STAR_END, STAR_START


class TestColor(unittest.TestCase):
    def test_special_star_band(self):
        for i in range(int(len(_SPECIAL_STARS) / 4)):
            s = random.choice(_SPECIAL_STARS)
            with self.subTest(i=s, msg=f"Special Star : {s}"):
                self.assertEqual(get_band(s), InternightBands.SPECIAL_STARS)

    def test_get_bands(self):
        # Test band for 20 stars
        for i in range(50):
            s = random.choice(range(STAR_START, STAR_END + 1))
            with self.subTest(msg=f"Testing band for star: {i}"):
                get_band(s)
