import json
from flask import Flask, request, jsonify

app = Flask(__name__)


def webhook_handler(request):
    """
    Webhook受信用のエンドポイント
    - challengeパラメータへの応答
    - ペイロードのログ出力
    - カスタム処理のためのプレースホルダー

    Args:
        request: Cloud Functions/Functions Frameworkから渡されるリクエストオブジェクト
    """
    try:
        payload = request.get_json()

        # challengeパラメータへの応答（Slack等のwebhook検証用）
        if "challenge" in payload:
            return jsonify({"challenge": payload["challenge"]})

        # ペイロードのログ出力
        print("Received webhook payload:")
        print(json.dumps(payload, indent=2, ensure_ascii=False))

        # TODO: ここにカスタム処理を実装してください
        # 例: payload["event"]["type"] に基づく処理分岐など

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ローカル開発用のFlaskアプリケーション
@app.route("/", methods=["POST"])
def flask_handler():
    return webhook_handler(request)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
