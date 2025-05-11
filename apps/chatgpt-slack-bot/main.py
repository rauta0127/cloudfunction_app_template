import os
import json
from openai import OpenAI
import requests
from flask import jsonify

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
SLACK_REPLY_URL = "https://slack.com/api/chat.postMessage"

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def send_slack_reply(channel: str, text: str, thread_ts: str = None):
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}", "Content-Type": "application/json"}
    payload = {"channel": channel, "text": text}
    if thread_ts:
        payload["thread_ts"] = thread_ts

    response = requests.post(SLACK_REPLY_URL, headers=headers, json=payload)
    print(f"[DEBUG] Slack response: {response.status_code} {response.text}")

    if response.status_code != 200 or not response.json().get("ok"):
        print(f"[ERROR] Slack通知失敗: {response.text}")
    else:
        print("[INFO] Slack通知成功")


def webhook_handler(request):
    try:
        # リトライ判定：Slackは再送時にこのヘッダーを付けてくる
        if request.headers.get("X-Slack-Retry-Num"):
            print("[INFO] Slack retry request detected. Skipping duplicate.")
            return jsonify({"status": "duplicate"}), 200

        data = request.get_json(silent=True)

        # SlackのURL検証（初回用）
        if "challenge" in data:
            return jsonify({"challenge": data["challenge"]})

        event = data.get("event", {})
        if event.get("type") != "app_mention":
            return jsonify({"status": "ignored"}), 200

        user_input = event.get("text", "")
        channel = event.get("channel", "")
        thread_ts = event.get("ts", "")

        # Botのメンション部分を取り除く（例: "<@UXXXXXX> こんにちは" → "こんにちは"）
        bot_user_id = data.get("authorizations", [{}])[0].get("user_id")
        if bot_user_id:
            user_input = user_input.replace(f"<@{bot_user_id}>", "").strip()

        # OpenAI Chat API に問い合わせ
        response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": user_input}])
        reply_text = response.choices[0].message.content
        # print(f"[DEBUG] ChatGPT応答: {reply_text}")

        # Slack に返信
        send_slack_reply(channel, reply_text, thread_ts=thread_ts)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"[ERROR] 処理失敗: {e}")
        return jsonify({"error": str(e)}), 500
