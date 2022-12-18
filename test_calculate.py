import unittest
import textwrap
from calculate import PersonWorkTime, calculate_all_person_work_time


class TestSlackBot(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_find_match_pattern(self):
        pwt_test = PersonWorkTime()
        msg_txt = textwrap.dedent(
            """\
            事務作業 6時間
            合計 6時間
            """
        )
        pwt_test.find_match_pattern_and_add_work_time(msg_txt)
        expected = PersonWorkTime(
            office_work={"pattern": "事務作業", "hour": 6},
            total={"pattern": "合計", "hour": 6}
        )
        self.assertEqual(pwt_test, expected)

    def test_calculate_all_person_work_time(self):
        pwt1 = PersonWorkTime(
            sales={"pattern": "営業", "hour": 5}
        )
        pwt2 = PersonWorkTime(
            sales={"pattern": "営業", "hour": 8},
            office_work={"pattern": "事務作業", "hour": 4}
        )
        pwt_list = [pwt1, pwt2]
        actual = calculate_all_person_work_time(pwt_list)
        # 営業時間が正しく取得できているか
        expected_sales_hour = 5 + 8
        self.assertEqual(actual.sales["hour"], expected_sales_hour)
        # 事務作業時間が正しく取得できているか
        expected_office_hour = 4
        self.assertEqual(actual.office_work["hour"], expected_office_hour)



if __name__ == "__main__":
    unittest.main()