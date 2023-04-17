import os
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from realtime_stock import get_realtime_quote, retro_price

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

line_bot_api.push_message(os.getenv('YOUR_USER_ID'),
                          TextSendMessage(text='你可以開始了'))


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
  # get X-Line-Signature header value
  signature = request.headers['X-Line-Signature']

  # get request body as text
  body = request.get_data(as_text=True)
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
  # message = TextSendMessage(text=event.message.text)
  #line_bot_api.reply_message(event.reply_token, message)
  message = event.message.text
  if re.match("早安", message):
    line_bot_api.reply_message(event.reply_token, TextSendMessage("早安~喵喵~"))
  elif re.match("你是誰",message):
    sticker_message = StickerSendMessage(
      package_id='1070',
      sticker_id='17878'
    )
    line_bot_api.reply_message(event.reply_token, sticker_message)
  elif re.match("新竹要去哪",message):
    location_message = LocationSendMessage( 
      title= "Big City遠東巨城購物中心",
      address= "新竹市東區中央路229號",
      latitude= 24.80999999772194, 
      longitude= 120.97512992065664
    )
    line_bot_api.reply_message(event.reply_token, location_message)
  elif re.match('回覆圖片',message):
    image_message = ImageSendMessage(
original_content_url='https://media.nownews.com/nn_media/thumbnail/2019/10/1570089924-27a9b9c9d7facd3422fe4610dd8ebe42-696x386.png',
    preview_image_url='https://media.nownews.com/nn_media/thumbnail/2019/10/1570089924-27a9b9c9d7facd3422fe4610dd8ebe42-696x386.png'
    )
    line_bot_api.reply_message(event.reply_token, image_message)
  elif re.match('回覆影片',message):
    video_message = VideoSendMessage(
      original_content_url='https://i.imgur.com/XVmZmIE.mp4',
      preview_image_url='https://img.ttshow.tw/images/media/frontcover/2020/08/06/6.jpg'
    )
    line_bot_api.reply_message(event.reply_token, video_message)
  elif re.match('回覆音檔',message):
    audio_message = AudioSendMessage(
      original_content_url='https://cdn.voicetube.com/everyday_records/5664/1626443219.mp3',
      duration=30000
    )
    line_bot_api.reply_message(event.reply_token, audio_message)
# 按鈕樣板
#   if "股票" in message:
#     buttons_template_message = TemplateSendMessage(
#     alt_text = "股票資訊",
#     template=CarouselTemplate( 
#     columns=[
#       CarouselColumn( 
#         thumbnail_image_url ="https://img.onl/0cAKyJ",
#         title = message[3:] + " 股票資訊", 
#         text ="請點選想查詢的股票資訊", 
#         actions =[
#           MessageAction( 
#             label= message[3:] + " 個股資訊",
#             text= "個股資訊 " + message[3:]),
#           MessageAction( 
#             label= message[3:] + " 個股新聞",
#             text= "個股新聞 " + message[3:]),
#         ]
#       ),
#       CarouselColumn( 
#           thumbnail_image_url ="https://img.onl/0cAKyJ",
#           title = message[3:] + " 股票資訊", 
#           text ="請點選想查詢的股票資訊", 
#           actions =[
#               MessageAction( 
#                   label= message[3:] + " 最新分鐘圖",
#                   text= "最新分鐘圖 " + message[3:]), 
#               MessageAction( 
#                   label= message[3:] + " 日線圖",
#                   text= "日線圖 " + message[3:]),  
#           ]
#       ),
#       CarouselColumn( 
#           thumbnail_image_url ="https://img.onl/0cAKyJ",
#           title = message[3:] + " 股利資訊", 
#           text ="請點選想查詢的股票資訊", 
#           actions =[
#               MessageAction( 
#                   label= message[3:] + " 平均股利",
#                   text= "平均股利 " + message[3:]),
#               MessageAction( 
#                   label= message[3:] + " 歷年股利",
#                   text= "歷年股利 " + message[3:])
#           ]
#       ),                               
#     ]
#     ) 
# )
#     line_bot_api.reply_message(event.reply_token, buttons_template_message)

# 快速回覆
  if '#' in message:
    flex_message = TextSendMessage(text="請選擇要顯示的資訊", 
                   quick_reply=QuickReply(items=[
                     QuickReplyButton(action=MessageAction(label="即時股價", text="即時股價: "+get_realtime_quote(message[1:]))),
                     QuickReplyButton(action=MessageAction(label="5日均價", text="5日均價: " + retro_price(message[1:],7))),
                     QuickReplyButton(action=MessageAction(label="20日均價", text="20日均價: " + retro_price(message[1:],30))),
                     QuickReplyButton(action=MessageAction(label="60日均價", text="60日均價: " + retro_price(message[1:],90))),
                     QuickReplyButton(action=MessageAction(label="1年均價", text="1年均價: " + retro_price(message[1:],365))),
                     QuickReplyButton(action=MessageAction(label="3年均價", text="3年均價: " + retro_price(message[1:],1095)))
                   ]))
    line_bot_api.reply_message(event.reply_token, flex_message)
  else: #回傳一模一樣的句子
    line_bot_api.reply_message(event.reply_token, TextSendMessage(message))


# 主程式
if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
