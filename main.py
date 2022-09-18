from email import message
from re import I
from flask import Flask, jsonify, request
from regex import R
import requests
from google.cloud import dialogflow
from requests_oauthlib import OAuth2
import os
import openai
import json
import firebase_admin
from firebase_admin import db,storage,firestore
from firebase_admin import credentials

cred = credentials.Certificate("sunmodza-cafe-firebase-adminsdk-bugkr-85cbeb7937.json")
firebase = firebase_admin.initialize_app(cred)
db = firestore.client()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "sunmodza-cafe-hbdc-eb4c4891fbd9.json"

from google.oauth2 import service_account
crediental = service_account.Credentials.from_service_account_file("sunmodza-cafe-hbdc-b41357c6e8ca.json")
#crediental = service_account.Credentials.from_service_account_file("sunmodza-cafe-hbdc-eb4c4891fbd9.json")

openai.api_key = "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"
project_id = "sunmodza-cafe-hbdc"

intents_client = dialogflow.IntentsClient(credentials=crediental)
#dialogflow.TrainAgentRequest()
parent = dialogflow.AgentsClient.agent_path(project_id)

app = Flask(__name__)

def create_intent(display_name, training_phrases_parts, payload,follow_intent=None):
    """Create an intent of the given intent type."""

    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    #text = dialogflow.Intent.Message.Text(text=message_texts)
    #json.dumps(payload)
    temp = False
    if not isinstance(payload,dict):
        message = payload
        temp = True
    else:
        message = dialogflow.Intent.Message(payload=payload)
    #message = dialogflow.Intent.from_json(json.dumps(payload))
    #message = dialogflow.Message.
    #print(message)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message],
        webhook_state = True
    )
    #apply_intent(intent)
    return intent

    #parent = dialogflow.AgentsClient.agent_path(project_id)
    #response = intents_client.create_intent(parent=parent, intent=intent)

    #print("Intent created: {}".format(response))

def apply_intent(intent):
    #if intent in not_in:
        #intents_client.delete_intent(intent)
    response = intents_client.create_intent(parent=parent, intent=intent)

import time


@app.route('/api',methods=["POST","GET"])
def hello():
    req = request.get_json()

    responseText = ""
    intent = req["queryResult"]["intent"]["displayName"]
    user_text = req["queryResult"]["queryText"]
    print(user_text)
    responseText = None


    if intent == "python":
        cmd = user_text[6:]
        print(cmd)
        responseText = str(eval(cmd))
    elif intent == "gpt":
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=user_text[4:],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        responseText = response["choices"][0]["text"]
    elif len(intent.split("-")) == 3:
        it = intent.split("-")
        print(it)
        #['originalDetectIntentRequest']['source']['userId']
        custumer_id = request.json['originalDetectIntentRequest']['payload']['data']['source']['userId']
        ref = db.collection("order_data").document(custumer_id)
        inner = f'{it[0]}-{it[1]}-{it[2]}'
        value = ref.get().to_dict()
        print(request.json['originalDetectIntentRequest']['payload']['data']['message']['text'])
        if request.json['originalDetectIntentRequest']['payload']['data']['message']['text'].split(" ")[-1] == "min":
            if value[inner][1] <= 1:
                ref.update({inner:firestore.DELETE_FIELD})
            else:
                ref.set({inner:[it[1],value[inner][1]-1,float(it[2])]},merge=True)
            responseText = "ลบเเล้วค่ะ"
        elif inner not in ref.get().to_dict():
            ref.set({inner:[it[1],1,float(it[2])]},merge=True)
        else:
            ref.set({inner:[it[1],value[inner][1]+1,float(it[2])]},merge=True)
        #time.sleep(2)
        value_updated = db.collection("order_data").document(custumer_id).get().to_dict()
        total = 0
        for i in value_updated:
            if i != "price":
                cost = value_updated[i][2] * value_updated[i][1]
                total+= cost
                continue
        ref.set({"price":total},merge=True)
        #db.collection("menu").document()
        pass
    
    elif intent == "cart":
        payload = create_cart()
        res = {"fulfillmentMessages": [payload]}
        #print(res)
        #print(res)
        return res
    
    elif intent == "promotion":
        ref = db.collection("promotion").stream()
        #value = ref.get().to_dict()
        objs = []
        for i in ref:
            data = i.to_dict()
            objs.append([i.id,data["img_uri"],data["describe"],data["order_this"]])
            #print(i.id,i.to_dict())
        #datas = [["sunmodza","https://raw.githubusercontent.com/sunmodza/datbakery_vc/main/cake/cake11.jpg","delight","เค้ก SMALL 500"]]
        payload = gen_promo(objs)
        res = {"fulfillmentMessages": [payload]}
        return res
    
    elif intent == "checkout":
        custumer_id = request.json['originalDetectIntentRequest']['payload']['data']['source']['userId']
        ref = db.collection("order_data").document(custumer_id)
        value = ref.get().to_dict()
        text = "name qty value\n"
        for i in value:
            if i != "price":
                name = i.split("-")[0]
                text += f" {name} {value[i][0]} - {value[i][1]} {value[i][2]*value[i][1]}\n"

        responseText = f"ท้้งหมด {value['price']} ค่ะ"

        
        

    # You can also use the google.cloud.dialogflowcx_v3.types.WebhookRequest protos instead of manually writing the json object
    res = {"fulfillmentMessages": [{"text": {"text": [responseText]}}]}

    return res

from menu_gen import gen_promo, gen_whole_menu,gen_cart
#r = requests.post(url, data = obj)
#print(r.json())

#dialogflow
#โกโก้	5	50		โกโก้, น้ำโกโก้	
b = create_intent("โกโก้37",["โกโกวา"],
      gen_whole_menu([["sunmodza", "https://raw.githubusercontent.com/sunmodza/datbakery_vc/main/cake/cake11.jpg", 3, "GOOD", [["SMALL", 500],["LARGE", 1000]]],
["sunmodza2", "https://raw.githubusercontent.com/sunmodza/datbakery_vc/main/cake/cake11.jpg", 3, "GOOD", [["SMALL", 500],["LARGE", 1000],["SUPER", 1500]]]])
)

def fetch_menu():
    menu_collection = db.collection("menu").stream()
    to_gen_menu = []
    all_intent = []

    for i in menu_collection:
        data = i.to_dict()
        #print(i.id,data)
        variation = [[key,data["variation"][key]["value"]] for key in data["variation"]]
        fmt = [i.id, data["img_uri"],data["rating"],data["describe"],variation]
        #print(fmt)
        to_gen_menu.append(fmt)
        print(data)
        for keyword in data["variation"]:
            #text = dialogflow.Intent.Message.Text(text=f'ได้ค่ะ {i.id} {keyword}')
            #message = dialogflow.Intent.Message(text=text)
            payload = {"line":{
                "type": "text",
                "text": f'ได้ค่ะ {i.id} {keyword}'
                }
                }
            follow_intent = create_intent(f'{i.id}-{keyword}-{data["variation"][keyword]["value"]}',[f'{i.id} {keyword} {data["variation"][keyword]["value"]}'],payload)
            all_intent.append(follow_intent)

    menu_intent = create_intent("เมนูโชว์5",["ขอดูเมนูหน่อยได้ป้ะ","เมนูจ้ะ"],gen_whole_menu(to_gen_menu))
    all_intent.append(menu_intent)

    return all_intent

def create_cart():
    custumer_id = request.json['originalDetectIntentRequest']['payload']['data']['source']['userId']
    data = db.collection("order_data").document(custumer_id).get().to_dict()
    datas = []
    for i in data:
        if i != "price":
            name = i.split("-")[0]
            #print(name,data[i])
            datas.append([name,data[i][0],data[i][2],data[i][1]])
    #print(datas)


    obj = gen_cart(datas,int(data["price"]))
    return obj
        


def create_all_menu_intent():
    all_intent = fetch_menu()
    all_intent_present_name = [intent.display_name for intent in all_intent]
    for intent in intents_client.list_intents(parent=parent):
        if intent.display_name in all_intent_present_name:
            try:
                intents_client.delete_intent(intent)
            except:
                pass
    for intent in all_intent:
        try:
            apply_intent(intent)
        except:
            pass
    


create_all_menu_intent()
# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    #create_cart()
    app.run(debug=True)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
