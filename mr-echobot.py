from flask import Flask, request
import json
import requests

app = Flask(__name__)

#Function handling GET requests
@app.route('/', methods=['GET'])
def handle_verification():
    print("Handling varification")
    if request.args.get('hub.verify_token','')=='my_voice_is_my_password_verify_me':
        print("Verification Successful!")
        return request.args.get('hub.challenge','')
    else:
        print("Verification failed!")
        return 'Error, wrong validation token'

#Function handling POST requests
@app.route('/', methods=['POST'])
def handle_messages():
    print("Handling messages")
    payload = request.get_data()
    print(payload)
    for sender, message in messaging_events(payload):
        print("Incoming from %s: %s" % (sender, message))
        return"ok"

def messaging_events(payload):
    """This function generates tuples of(sender_id, message_text) from the provided payload"""
    data=json.loads(payload)
    messagin_events=data["entry"][0]["messaging"]
    for event in messagin_events:
       if "message" in event and "text" in event["message"]:
        yield event["sender"]["id"], event["message"] ["text"].encode('unicode_escape')  #So that items like emoji which are encoded are not sent back as garbage.It will be decode in next func.
       else:
           yield event["sender"]["id"], "I can't echo this"

    def send_message(token, recipient, text):
                #Sends the msg text to recipent with id recipient
        r=requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps({
      "recipient": {"id": recipient},
      "message": {"text": text.decode('unicode_escape')}
    }),
    headers={'Content-type': 'application/json'})
    if r.status_code!=requests.codes.ok:
       print(r.text)





if __name__ == '__main__':
    app.run()
