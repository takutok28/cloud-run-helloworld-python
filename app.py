#!/usr/bin/python
import os
import json

from flask import Flask, request

app = Flask(__name__)

# 詳細はhttps://cloud.google.com/logging/docs/setup/python
# Cloud Logging client Libraryをインストール
import google.cloud.logging

# クライアントをインスタンス化
client = google.cloud.logging.Client()
logger = client.logger('Cloud Run Logger')

# Pythonのロギングモジュールと統合
client.setup_logging()

PROJECT = "beam-logging-monitoring-demo"

@app.route('/')
def hello_world():
    logger.log_text('Hello World')
    print("これは標準出力によるprintです。")
    return 'Hello World!\n'

@app.route('/error')
def hello_world():
    logger.error('エラーが発生しました')

@app.route('/warning')
def warning():
    logger.warning('警告')
    
@app.route('/trace')
def trace():
    """
    Cloud Traceとの連携
    """
    #デフォルトでCloud Runに対するリクエストに含まれている
    trace_header = request.headers.get("X-Cloud-Trace-Context")
    # traceフィールドは、projects/[PROJECT_ID]/traces/[TRACE_ID]
    trace = trace_header.split("/")
    log_entry = {
        "logging.googleapis.com/trace": f"projects/{PROJECT}/traces/{trace[0]}",
        "message" : "Cloud Traceとの連携",
        "severity":"NOTICE"
    }

    print(json.dump(log_entry))

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
