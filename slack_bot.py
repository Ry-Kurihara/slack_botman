import os
from typing import List, Dict, Iterator, Any
from dataclasses import dataclass, field
import re 
# Not standard
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


# ボットトークンと署名シークレットを使ってアプリを初期化します
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
token = os.environ["SLACK_BOT_TOKEN"]

@app.message("計算")
def calculate_work_time(client, message, say):
    channel_id = message["channel"]
    thread_ts = message["thread_ts"]
    thread_msgs = client.conversations_replies(token=token, channel=channel_id, ts=thread_ts)["messages"]
    pwt_list = list(_calculate_working_time_from_thread_msgs(thread_msgs))
    all_pwt = _calculate_all_person_work_time(pwt_list)
    reply_msg = _create_message_from_pwt_object(all_pwt)
    say(reply_msg, thread_ts=thread_ts)

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

    def _get_ins_var_keys(self) -> List[str]:
        return list(self.__dict__.keys())

    def _get_ins_var_values(self) -> List[Dict[str, Any]]:
        return list(self.__dict__.values())

    def __add__(self, other):
        values = self._get_ins_var_values()
        other_values = other._get_ins_var_values()
        for value, other_value in zip(values, other_values):
            value["hour"] += other_value["hour"]
        return self
            
    def _find_match_pattern_and_add_work_time(self, message_text: str) -> None:
        values = self._get_ins_var_values()
        for value in values:
            calculate_class = value["pattern"]
            pattern = rf"[\s\S]*{calculate_class}\s([0-9]+)時間[\s\S]*"
            if m := re.match(pattern, message_text):
                hour = int(m.group(1))
                value["hour"] += hour

def _calculate_working_time_from_thread_msgs(thread_msgs: List[Dict]) -> Iterator[PersonWorkTime]:
    for msg in thread_msgs:
        pwt = PersonWorkTime()
        msg_txt = msg["text"]
        pwt._find_match_pattern_and_add_work_time(msg_txt)
        yield pwt 

def _calculate_all_person_work_time(pwt_list: List[PersonWorkTime]) -> PersonWorkTime:
    all_pwt = PersonWorkTime()
    for pwt in pwt_list:
        all_pwt += pwt
    return all_pwt

def _create_message_from_pwt_object(pwt: PersonWorkTime) -> str:
    message = ""
    values = pwt._get_ins_var_values()
    for value in values:
        message_line = f"{value['pattern']} {value['hour']}時間\n"
        message += message_line
    return message


# アプリを起動します
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()