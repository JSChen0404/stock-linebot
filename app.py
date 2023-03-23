# 載入LineBot所需要的模組
import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi(
    'ptbE+JR3/YkHqATTSSftUhoKzpH2SMJ35+CobNMRw9faw3FVb0acaDYlN7oQxX9fuM5nuG3TIavIy/xJQPy0p4AO2UlK9dZ2wvzOoz/YbrJqql00Y3/6nLhERvudqYipxI9Ub1pxQJvx/p91m5kM8wdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('3bd50273d59d1f70bb71b314dec4c111')

line_bot_api.push_message(
    'U9033841fbbfe66347373576c24ca6e8a', TextSendMessage(text='你可以開始了'))


# Webhook settings最後設定!!!!!!!!!!!!!!!!!!

# 訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)


# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
