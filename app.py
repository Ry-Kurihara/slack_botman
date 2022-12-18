import os
from calculate import calculate_working_time_from_thread_msgs
from calculate import calculate_all_person_work_time, create_message_from_pwt_object

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
    pwt_iter = calculate_working_time_from_thread_msgs(thread_msgs)
    all_pwt = calculate_all_person_work_time(pwt_iter)
    reply_msg = create_message_from_pwt_object(all_pwt)
    say(reply_msg, thread_ts=thread_ts)


# アプリを起動します
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()