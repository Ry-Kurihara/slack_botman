from typing import List, Dict, Iterator, Iterable, Any 
from dataclasses import dataclass, field
import re 

@dataclass
class PersonWorkTime:
    sales: Dict[str, Any] = field(
        default_factory = lambda: {"pattern": "営業", "hour": 0}
    )
    office_work: Dict[str, Any] = field(
        default_factory = lambda: {"pattern": "事務作業", "hour": 0}
    )
    phone_support: Dict[str, Any] = field(
        default_factory = lambda: {"pattern": "電話対応", "hour": 0}
    )
    total: Dict[str, Any] = field(
        default_factory = lambda: {"pattern": "合計", "hour": 0}
    )

    def get_ins_var_keys(self) -> List[str]:
        return list(self.__dict__.keys())

    def get_ins_var_values(self) -> List[Dict[str, Any]]:
        return list(self.__dict__.values())

    def __add__(self, other):
        values = self.get_ins_var_values()
        other_values = other.get_ins_var_values()
        for value, other_value in zip(values, other_values):
            value["hour"] += other_value["hour"]
        return self
            
    def find_match_pattern_and_add_work_time(self, message_text: str) -> None:
        values = self.get_ins_var_values()
        for value in values:
            calculate_class = value["pattern"]
            pattern = rf"[\s\S]*{calculate_class}\s([0-9]+)時間[\s\S]*"
            if m := re.match(pattern, message_text):
                hour = int(m.group(1))
                value["hour"] += hour

def calculate_working_time_from_thread_msgs(thread_msgs: List[Dict]) -> Iterator[PersonWorkTime]:
    for msg in thread_msgs:
        pwt = PersonWorkTime()
        msg_txt = msg["text"]
        pwt.find_match_pattern_and_add_work_time(msg_txt)
        yield pwt 

def calculate_all_person_work_time(pwt_iter: Iterable[PersonWorkTime]) -> PersonWorkTime:
    all_pwt = PersonWorkTime()
    for pwt in pwt_iter:
        all_pwt += pwt
    return all_pwt

def create_message_from_pwt_object(pwt: PersonWorkTime) -> str:
    message = "ウィーーーン...\n"
    values = pwt.get_ins_var_values()
    for value in values:
        message_line = f"{value['pattern']} {value['hour']}時間\n"
        message += message_line
    return message