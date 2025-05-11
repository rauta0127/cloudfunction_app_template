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
# または
.venv\Scripts\activate  # Windowsの場合
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
gcloud functions deploy webhook_receiver_sample \
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