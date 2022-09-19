from flask import json, Flask, request, Response, abort
import json, requests
from webexteamssdk import WebexTeamsAPI
import datetime

#api = WebexTeamsAPI()
global value

def webexAlert(authorName , email , date ,message ,url , pullUrl ,check):
    addMessageURL= 'https://webexapis.com/v1/messages'
    headers={
        "Authorization": "Bearer NGJlYWViYWQtNDQ4Yy00M2M1LTg5ZTUtZGYyMjZhYjA0Y2RhNmIwYjIyMWYtYzg4_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f",
        "Content-Type": "application/json"
    }
    roomId= "Y2lzY29zcGFyazovL3VzL1JPT00vMDdjZmE2NTAtMDQ5NS0xMWVjLTlkZDctMzlmMDI2OWYyODc5"
    if check == 1:
        addMessage={
              "roomId": roomId,
              "markdown": "[Tell us about yourself](https://www.example.com/form/book-vacation). We just need a few more details to get you booked for the trip of a lifetime!",
              "attachments": [
                {
                      "contentType": "application/vnd.microsoft.card.adaptive",
                      "content": 
                {
                        "type": "AdaptiveCard",
                        "version": "1.0",
                        "body": [
                        {
                                "type": "Container",
                                "items": [
                                {
                                        "type": "TextBlock",
                                        "text": "Changes made in pull request"
                                },
                                {
                                        "type": "Input.Text",
                                        "placeholder": pullUrl,
                                        "inlineAction": {
                                            "type": "Action.OpenUrl",
                                "url": pullUrl,
                                "title": "Go"
                                        }
                                },
                                {
                                        "type": "ColumnSet",
                                        "columns": [
                                        {
                                                "type": "Column",
                                                "width": "stretch",
                                                "items": [
                                                {
                                                        "type": "TextBlock",
                                                        "text": "Author Name:"
                                                }
                                                ]
                                        },
                                        {
                                                "type": "Column",
                                                "width": "stretch",
                                                "items": [
                                                {
                                                        "type": "Input.Text",
                                                        "placeholder": authorName,
                                                        "isMultiline": True
                                                }
                                                ]
                                        }
                                        ]
                                },
                                {
                                        "type": "ColumnSet",
                                        "columns": [
                                        {
                                                "type": "Column",
                                                "width": "stretch",
                                                "items": [
                                                {
                                                        "type": "TextBlock",
                                                        "text": "Author Email:"
                                                }
                                                ]
                                        },
                                        {
                                                "type": "Column",
                                                "width": "stretch",
                                                "items": [
                                                {
                                                        "type": "Input.Text",
                                                        "placeholder": email,
                                                        "isMultiline": True
                                                }
                                                ]
                                        }
                                        ]
                                },
                                {
                                        "type": "ColumnSet",
                                        "columns": [
                                        {
                                                "type": "Column",
                                                "width": "stretch",
                                                "items": [
                                                {
                                                        "type": "TextBlock",
                                                        "text": "Date:"
                                                }
                                                ]
                                        },
                                        {
                                                "type": "Column",
                                                "width": "stretch",
                                                "items": [
                                                {
                                                        "type": "Input.Text",
                                                        "placeholder": date,
                                                        "isMultiline": True
                                                }
                                                ]
                                        }	
                                        ]
                                },
                                {
                                        "type": "ColumnSet",
                                        "columns": [
                                        {
                                                "type": "Column",
                                                "width": "stretch",
                                                "items": [
                                                {
                                                        "type": "TextBlock",
                                                        "text": "Message:"
                                                }
                                                ]
                                        },
                                        {
                                                "type": "Column",
                                                "width": "stretch",
                                                "items": [
                                                {
                                                        "type": "Input.Text",
                                                        "placeholder": message,
                                                        "isMultiline": True
                                                    }
                                                ]
                                        }
                                        ]
                                },
                                {
                                        "type": "ColumnSet",
                                        "columns": [
                                        {
                                                "type": "Column",
                                                "width": "stretch",
                                                "items": [
                                                {
                                                        "type": "TextBlock",
                                                        "text": "URL:"
                                                }
                                                ]
                                        },
                                        {
                                                "type": "Column",
                                                "width": "stretch",
                                                "items": [
                                                {
                                                        "type": "Input.Text",
                                                        "placeholder": url,
                                                        "isMultiline": True,
                                    "inlineAction": {
                                                            "type": "Action.OpenUrl",
                                                            "url": url,
                                        "title": "Go"
                                                        }
                                                }
                                                ]
                                        }
                                        ]
                                }
                                ],
                                "horizontalAlignment": "Center",
                                "height": "stretch",
                                "spacing": "Padding",
                                "style": "emphasis"
                        }
                        ],
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "minHeight": "200px"
                }
            }
            ]
        }
    else:
        addMessage={
            "roomId":roomId,
            "text": "Pull Request successfully merged"
        }
    posts=requests.post(addMessageURL, data=json.dumps(addMessage), headers=headers)
    #api.messages.create(roomId, text="Welcome to the room!")
    

app = Flask(__name__)

@app.route('/github', methods=['POST'])
def respond():
    if request.method == 'POST':
        data=json.dumps(request.json)
        if "pull_request" in data:
            if request.json['action'] == 'opened':
                check=1
                value=request.json['pull_request']['commits_url']
                pullUrl=request.json['pull_request']['html_url']
                r=requests.get(value)
                jsonFile=r.json()
                jsonFile=jsonFile[0]
                authorName =jsonFile.get('commit').get('author').get('name')
                email =jsonFile.get('commit').get('author').get('email')
                date =jsonFile.get('commit').get('author').get('date')
                #d1 = datetime.datetime.strftime(date,"%Y-%m-%dT%H:%M:%SZ")
                #new_format = "%Y-%m-%d"
                #d1.strftime(new_format)
                message =jsonFile.get('commit').get('message')
                url =value
                finalMessage="Author Name: "+authorName+"\n"+"Author email: "+email+"\n"+"Created Date: "+date+"\n"+"Message: "+message+"\n"+"URL: "+url
                #authorName=jsonFile.get('commit')
                print(request.json)
                print(finalMessage)
                webexAlert( authorName , email , date ,message ,url, pullUrl ,check)
            else:
                check=0
                webexAlert("","", "","" ,"","" ,check)
        return '',200
    else:
        abort(400)

if __name__=='__main__':
    app.run(debug=True)