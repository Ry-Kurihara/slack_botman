import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from typing import List, Dict, Union
from dataclasses import dataclass, field
import pdb 
import re 

# ボットトークンと署名シークレットを使ってアプリを初期化します
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# 'hello' を含むメッセージをリッスンします
@app.message("hello")
def message_hello(message, say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text":"Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

token = os.environ["SLACK_BOT_TOKEN"]
@app.message("uho")
def test_client(client, message):
    channel_id = message["channel"]
    print(f"message:{message}")
    thread_ts = message["thread_ts"]
    print(f"thread_ts: {thread_ts}")
    client.chat_postMessage(token=token, channel=channel_id, text="ウッヒョおおおおおお")

    # スレッドメッセージの取得
    thread_msgs = client.conversations_replies(token=token, channel=channel_id, ts=thread_ts)["messages"]
    pwt_list = list(_calculate_working_time_from_thread_msgs(thread_msgs))

    

@dataclass
class PersonWorkTime:
    sales: Dict[str, Union[str, int]] = field(
        default_factory = lambda: {"pattern": "営業", "hour": 0}
    )
    office_work: Dict[str, Union[str, int]] = field(
        default_factory = lambda: {"pattern": "事務作業", "hour": 0}
    )
    phone_support: Dict[str, Union[str, int]] = field(
        default_factory = lambda: {"pattern": "電話対応", "hour": 0}
    )
    total: Dict[str, Union[str, int]] = field(
        default_factory = lambda: {"pattern": "合計", "hour": 0}
    )


    def _find_match_pattern_and_add_work_time(self, message_text: str) -> None:
        class_items = self.__dict__.items()  
        for class_item in class_items:
            # class_item: ('sales', {'pattern': '営業', 'hour': 0})みたいな中身になっている
            calculate_class = class_item[1]["pattern"]
            print(f"クラス：{calculate_class}")
            pattern = rf"[\s\S]*{calculate_class}\s([0-9]+)時間[\s\S]*"
            if m := re.match(pattern, message_text):
                # TODO: ここの書き方！！！！
                print(f"テキスト：{message_text}")
                hour = m.groups()[0]
                class_item[1]["hour"] += int(hour) 




def _calculate_working_time_from_thread_msgs(thread_msgs: List[Dict]) -> PersonWorkTime:
    for msg in thread_msgs:
        pwt = PersonWorkTime()
        msg_txt = msg["text"]
        print(f"thread_message解析中・・・: {msg_txt}")
        pwt._find_match_pattern_and_add_work_time(msg_txt)
        yield pwt 



@app.action("button_click")
def action_button_click(body, ack, say):
    # アクションを確認したことを即時で応答します
    ack()
    # チャンネルにメッセージを投稿します
    say(f"<@{body['user']['id']}> clicked the button")

# アプリを起動します
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()