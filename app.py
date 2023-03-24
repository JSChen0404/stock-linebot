import os
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

line_bot_api.push_message(os.getenv('YOUR_USER_ID'),
                          TextSendMessage(text='replit start!'))


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
  signature = request.headers[
    'X-Line-Signature']  # get X-Line-Signature header value
  body = request.get_data(as_text=True)  # get request body as text
  app.logger.info("Request body: " + body)

  # handle webhook body
  try:
    handler.handle(body, signature)
  except InvalidSignatureError:
    abort(400)

  return 'OK'


# 訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
import re


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  message = event.message.text  # 利用「.text」取出傳來的訊息
  if re.match("你是誰", message):
    line_bot_api.reply_message(event.reply_token, TextSendMessage("才不告訴你勒~~"))
  else:
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(message))  # 這句話重複使用者的回覆
  # event.reply_token為產生接收訊息的token
  # message為預計回傳給使用者的訊息，必須加上TextSendMessage


# 主程式
if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
