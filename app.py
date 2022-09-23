#載入LineBot所需要的模組
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *


app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('dMNPHD5kzKtJ6P2d82I75GHcdP0N5pFu4WtVGKEbMge')

# 必須放上自己的Channel Secret
handler = WebhookHandler('f51ff004b20891f9090a35f451f09e91')




# def lineNotifyMessage(token, msg):
#     headers = {
#         "Authorization": "Bearer " + token, # 權杖，Bearer 的空格不要刪掉呦
#         "Content-Type": "application/x-www-form-urlencoded"
#     }

#     payload = {'message': msg}
    
#     # Post 封包出去給 Line Notify
#     r = requests.post(
#         "https://notify-api.line.me/api/notify",
#         headers=headers, 
#         params=payload)
#     return r.status_code

#推播
#你自己的ID="U1ea6cc7b8d57118cfc096f69509ca9ed"
#line_bot_api.push_message('你自己的ID', TextSendMessage(text='你可以開始了'))

'''
我們的程式碼是要放到heroku中，因此我們也需要讓heroku跟LINE Bot做串接才行，因此我們先加上如下的程式碼，主要是回報我們串接是否成功
'''

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


#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)
#而最後我們就必須執行程式碼，所以記得加上以下的程式碼，以表示執行
#主程式
import os 
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)