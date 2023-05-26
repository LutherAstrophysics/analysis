import unittest

from trout.color import *  # noqa F403
from trout.conversions import *  # noqa F403
from trout.database import *  # noqa F403
from trout.exceptions import *  # noqa F403
from trout.files import *  # noqa F403
from trout.greet import *  # noqa F403
from trout.internight import *  # noqa F403
from trout.nights import *  # noqa F403
from trout.stars import *  # noqa F403
from trout.vis import *  # noqa F403


class TestCircularImport(unittest.TestCase):
    def test_import(self):
        pass
