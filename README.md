# slack_botman

簡単なスレッド内数値計算アプリです。

### 必要なScope
- Bot Token Scopes
    - channels:history
        - スレッド内のメッセージを取得するために必要です。
    - chat:write
        - Botが計算結果を書き込むために必要です。
- App-Level-Tokens
    - connections:write
        - ソケットモード通信で発生したSlackイベントを受け取るために必要です。