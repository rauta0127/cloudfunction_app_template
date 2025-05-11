# Webhook Receiver Template

このテンプレートは、Cloud Functions上で動作する汎用的なWebhook受信処理の雛形を提供します。
Slack、Stripe、GitHubなどのWebhookに対応しており、簡単にカスタマイズして使用できます。

## 機能

- HTTP POSTエンドポイントの提供
- Webhook検証用のchallenge応答機能
- ペイロードのログ出力
- カスタム処理のためのプレースホルダー

## ローカル開発

1. 仮想環境の作成と有効化:
```bash
python -m venv .venv
source .venv/bin/activate  # Linuxの場合
```

2. 依存関係のインストール:
```bash
pip install -r requirements.txt
pip install functions-framework
```

3. ローカルサーバーの起動:
```bash
functions-framework --target webhook_handler --debug
```

## デプロイ

Cloud Functionsへのデプロイ:

```bash
gcloud functions deploy chatgpt-slack-bot \
  --gen2 \
  --runtime=python311 \
  --region=asia-northeast1 \
  --source=. \
  --entry-point=webhook_handler \
  --trigger-http \
  --memory=512MB
```

## カスタマイズ

`main.py`の`webhook_handler`関数内のTODOコメント部分に、必要な処理を実装してください。
一般的な実装例:

- イベントタイプに基づく処理分岐
- 外部APIとの連携
- データベースへの保存
- 通知の送信

## 注意事項

- 本番環境では適切な認証・認可の実装を推奨します
- 機密情報は環境変数として管理してください
- エラーハンドリングを適切に実装してください 


## テンプレート検証手順（開発者向け）

このテンプレートが正しく機能するかを確認するための、ローカル検証手順です。

### 🛠 ステップ① テンプレートが正しく生成できるか確認

```bash
# 仮想環境の準備（1回だけ）
cd cloudfunction_app_template
python3 -m venv .venv
source .venv/bin/activate
pip install cookiecutter
```

# テンプレートから新しいアプリを生成
```
cookiecutter templates/webhook_receiver/

# 正しくファイルが生成されているか確認
tree webhook_receiver_sample/
# → main.py, requirements.txt, function_config.yaml, README.md があること
```

### 🧪 ステップ② アプリのローカル動作確認
```
# 生成したアプリのディレクトリに移動
cd webhook_receiver_sample
```

```
# 仮想環境を作成し依存をインストール
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install functions-framework
```

# ローカルで関数を起動
```
functions-framework --target=webhook_handler
```

# 別ターミナルでテスト用リクエストを送信
```
curl -X POST http://localhost:8080/ \
  -H "Content-Type: application/json" \
  -d '{"challenge": "abc123"}'
```
→ "abc123" がレスポンスとして返ればOK（SlackのURL検証に対応）

### ☁️ ステップ③ GCP へのデプロイ（任意）
```
gcloud functions deploy webhook_receiver_sample_gen2 \
  --gen2 \
  --runtime=python311 \
  --region=asia-northeast1 \
  --entry-point=webhook_handler \
  --trigger-http \
  --memory=512Mi \
  --timeout=60s \
  --allow-unauthenticated
```


