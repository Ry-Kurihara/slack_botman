import unittest
from unittest.mock import patch
import textwrap

from app import PersonWorkTime


class TestSlackBot(unittest.TestCase):
    def setup(self):
        self.bolt_app_m = patch("app.slack_bolt.App")
        
    def tearDown(self):
        patch.stopall()

    def test_find_match_pattern(self):
        pwt = PersonWorkTime()
        msg_txt = textwrap.dedent(
            """\
            事務作業 2時間
            合計 3時間
            """
        )
        pwt._find_match_pattern_and_add_work_time(msg_txt)
        # 事務作業時間が正しく取得できているか
        correct_office_hour = 2
        self.assertEqual(correct_office_hour, pwt.office_work["hour"])
        # 合計時間が正しく取得できているか
        correct_total_hour = 3
        self.assertEqual(correct_total_hour, pwt.total["hour"])

if __name__ == "__main__":
    unittest.main()