from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import pandas as pd
from JobSeeker import JobSeeker

lineBotApi = LineBotApi('GpHGU2aSziozCYXtU8DoSoqU/4t7S2ih12VIRVWTlzjXWz9kFE+OLvT8sb/tcszZc5gEigD1Plky+qN8f5A84rvC8Sq2nDESiACTx3D3d3S/8CSdcJQUmMfrNSzQYcQDDzeACZn8527KIM38GiE/PQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1940915c9e9e8d423a3b5ca0cf781669')

@app.route("/")
def hello_world():
    print("hello world!")
    return "<p>Hello!</p>"

@app.route("/callback", methods=["POST"])
def callback():
    print("callback")
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = str(event.message.text)
    print("handling message: " + text)
    resp = []
    
    if "j" == text.lower() or "job" == text.lower() or "jobs" == text.lower() or "jobseeker" == text.lower():
        try:
            preword = "For each company, at most 10 fulltime jobs associated with computer science are listed."
            resp.append(TextSendMessage(preword))
            js = JobSeeker()
            
            googleResult = "Google results:\n"
            googleResult += js.seekGoogle()
            resp.append(TextSendMessage(googleResult))
            
            microsoftResult = "Microsoft results:\n"
            microsoftResult += js.seekMicrosoft()
            resp.append(TextSendMessage(microsoftResult))
            
            print("Sending " + str(len(resp)) + " resp message.")
            lineBotApi.reply_message(event.reply_token, resp)
        except Exception as e:
            lineBotApi.reply_message(event.reply_token, TextSendMessage(text="Job Seeker failed with exception:\n" + str(e)))
            
    else:
        lineBotApi.reply_message(event.reply_token, TextSendMessage(text="Not supported command:\n" + text + ""))


if __name__ == '__main__':
    app.run(port=5001)