import json
import datetime
import time
import os
import dateutil.parser
import logging


def lambda_handler(event, context):
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    return dispatch(event)

def dispatch(intent_request):
    intent_name = intent_request['currentIntent']['name']
    user_input = str(intent_request['inputTranscript'])
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    
    if intent_name == "ShowerGoal":
        if user_input == "One to eight minutes":
            reply = "Great!! Avg American water usage is 17.2 gallon with shower length being about 8 min. You are saving water as well as life."
        elif user_input == "Nine to Fifteen minutes":
            reply = "Good job. But you could be doing better! Avg American water usage is 17.2 gallon with shower length being about 8 min. If you conserve water, you conserve life."
        else:
            reply = "The avarage American water usage is 17.2 gallon with shower length being about 8 min. Just remember, if you do not save water, we will all be like a fish out of water!"
    
        
        next_intent = "ElectricityIntent"
        
    elif intent_name == 'ElectricityIntent':
        if user_input == "I always switch off light and electric appliance before leaving":
            reply = "Congrats! You are doing your part to conserve energy and saving on your electricity bill. #GuiltFree"
        elif user_input == "I occasionally switch off the light and electric appliance ":
            reply = "You can do better! Just cut down 5 minutes and save yourself a fortune on your electricity bill."
        else:
            reply = "Go and try it! Go save the Earth and your electricity bill."
        
        next_intent = "RecycleIntent"
    
    elif intent_name == 'RecycleIntent':
        if user_input == "Once a day":
            reply = "Thank you for making a huge effort in keeping our planet healthy! Remember, you  truly do make a huge difference."
        elif user_input == "Once a week":
            reply = "Good, try and do it every day to make sure the organisms and our planet stays healthy."
        else:
            reply = "That is not good. Did you know that humans are producing 127,604 Lbs of waste every year!"
        
        next_intent = "FinishIntent"
        
    elif intent_name == 'FinishIntent':
        if user_input == "Conserving water":
            reply = "Thats great! You will be helping the oceans and fish alot! Also, thanks for using our bot"
        elif user_input == "Conserving electricity":
            reply = "Great job and keep it up. Also, thanks for using our bot"
        else:
            reply = "Keep up the good usage! You will be saving alot of money this way. Also, thanks for using our bot"
        
    return close(session_attributes,'Fulfilled', reply, getCard(next_intent))

def getCard(type):
    if type == "RecycleIntent":
        responseCard = {
            "contentType": "application/vnd.amazonaws.card.generic",
            "version": "1",
            "genericAttachments": [
              {
                "attachmentLinkUrl": None,
                "buttons": [
                  {
                    "text": "I recycle everyday",
                    "value": "Once a day"
                  },
                  {
                    "text": "I recycle every week",
                    "value": "Once a week"
                  },
                  {
                    "text": "I dont recycle",
                    "value": "I dont recycle"
                  }
                ],
                "imageUrl": "https://cdn.pixabay.com/photo/2014/03/24/13/42/recycling-294079__340.png",
                "subTitle": "Recycle",
                "title": "Do you recycle?"
              }
            ]
        
            
        }
        return responseCard

    if type == "ElectricityIntent":
        responseCard =  {
            "contentType": "application/vnd.amazonaws.card.generic",
            "version": "1",
            "genericAttachments": [
                {
                  "attachmentLinkUrl": None,
                  "buttons": [
                      {
                        "text": "I always switch off light and electric appliance before leaving",
                        "value":"I always switch off light and electric appliance before leaving"
                      },
                      {
                        "text": "I occasionally switch off the light and electric appliance ",
                        "value": "I occasionally switch off the light and electric appliance "
                      },
                      {
                        "text": "I only sometime switch off the light and electric appliance ",
                        "value": "I only sometime switch off the light and electric appliance "
                      }
                    ],
                    "imageUrl": "https://i.ytimg.com/vi/MzDIkkgcLiw/maxresdefault.jpg",
                    "subTitle": "Electricity",
                    "title": "How much electricity do you use?"
                  }
                ]
                
                
            }
        return responseCard
        
    if type == "FinishIntent":
        responseCard =  {
                "contentType": "application/vnd.amazonaws.card.generic",
                "version": "1",
                "genericAttachments": [
                  {
                    "attachmentLinkUrl": None,
                    "buttons": [
                          {
                            "text": "Conserving water",
                            "value": "Conserving water"
                          },
                          {
                             "text": "Conserving electricity",
                             "value": "Conserving electricity"
                          },
                          {
                             "text": "Recycling",
                             "value": "Recycling"
                          }
                         ],
                        "imageUrl": "http://4.bp.blogspot.com/-gIS_bwTmPks/Ud-2L9x-pYI/AAAAAAAAALY/gxODC_qfgz4/s1600/Fotolia_44112639_Subscription_Monthly_M.jpg",
                        "subTitle": "Reflection",
                        "title": "Tell me one area which are willing to do more for enviornment ?" 
                  }
                ]
                            
            }
        return responseCard
    
    return None

def close(session_attributes, fulfillment_state, message, responseCard = None):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': 
                {
                  "contentType": "PlainText",
                  "content": message
                }
            }
        }
    if responseCard != None : 
        response["dialogAction"]["responseCard"] = responseCard
        response["dialogAction"]["message"]["contentType"] = "SSML"
    
    return response