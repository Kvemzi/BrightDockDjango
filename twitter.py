#Imports:
import json
import os
import requests
import websockets
from websocket import create_connection
import json


#Authentication for twitter dev accout through Bearer token:
file = open("BearerToken.txt",'r')
os.environ['TOKEN'] =  file.read()

#Function for returning auth token
def auth():
    return os.getenv('TOKEN')
bearer_token = auth()


#Creating headers for twitter so I can eneter with authorization
def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers
headers = create_headers(bearer_token)


#Creating twitter url for reqeuest method
def create_url(keyword, max_results = 10):
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    query_params ={
        'query':keyword,
        'max_results':max_results,
        'expansions':'author_id',
        'user.fields': 'id,name,username',
        'tweet.fields':'id,text,author_id,created_at',
    }
    return(search_url,query_params)
keyword = "#FIFA"
max_results = 10
url = create_url (keyword,max_results)


#Gathering data from twitter for multiple tweets throufgh url,headers, and params
def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
json_response = connect_to_endpoint(url[0], headers, url[1])
test = json.dumps(json_response, indent = 4, sort_keys = True)
solution =  []
print("Solutions for: " + keyword)


#Gathering tweet field if tweet filed from searching multiple tweets hase over 230 characters
def connect_to_endpoint2(url, headers):
    params = {}
    params['tweet.fields'] ='text' 
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()




#Reading the collected data and writing is to a list
#solutions with dict atribute
#soluition = [{mmessage, author_id, tweet_id, created_at, author_name, author_username, tweet_url}]
for i in range(0,len(json_response['data'])):
    if len(json_response['data'][i]['text']) > 230:
        url = 'https://api.twitter.com/2/tweets/' + str(json_response['data'][i]['id'])
        json_response2 =connect_to_endpoint2(url,headers)
        message = json_response2['data']['text']
    else:
        message = json_response['data'][i]['text']
    author_id = json_response['data'][i]['author_id']
    tweet_id = json_response['data'][i]['id']
    created_at = json_response['data'][i]['created_at']
    for j in json_response['includes']['users']:
        if(author_id == j['id']):
            author_name = j['name']
            author_username = j['username']
            tweet_url = 'https://twitter.com/' + str(author_username) + '/status/' + str(tweet_id)
            break
        
    solution.append({
        'author_id':author_id,
        'tweet_id':tweet_id,
        'tweet':message,
        'created_at':created_at,
        'author_name':author_name,
        'author_username':author_username,
        'url_to_tweet':tweet_url
    })

#Getting data from server which I have uploaded earlier
def connect_to_endpoint3 ():
    params = {'tweet_id'}
    url = 'http://0.0.0.0:8000/twitter/'
    response = requests.request("GET", url)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
json_response3 = connect_to_endpoint3()
duplicates = []
for a in json_response3:
    duplicates.append(a['tweet_id'])




#Deleting tweets which are older than collectd tweets
list_of_keys=[]
url = 'http://0.0.0.0:8000/twitter/'
for i in solution:
    list_of_keys.append(i['tweet_id'])
    print(type(i['tweet_id']))
for i in duplicates:
    if str(i) not in list_of_keys:
        requests.delete(url + str(i))


#Removing unneceseary duplicates
def remove_duplicates():
    for i in duplicates:
        for j in range(0,len(solution)):
            try:
                if str(solution[j]['tweet_id']) == str(i):
                    solution.pop(j)
            except ValueError:
                pass

remove_duplicates()



#Uploading data on server via POST request
def give_the_data(data):
    url = 'http://0.0.0.0:8000/twitter/'
    i = 0
    for obj in data:
        x = requests.post(url, json=obj)
        if x.status_code !=201:
            raise Exception(x.status_code, x.text)
        i+=1
        print(i)
give_the_data(solution)



#Sending tweets to WebSocket
def send_to_ws(tweet):
    ws = create_connection("ws://127.0.0.1:8000/ws/chat/lobby/")
    message = tweet
    text_data=json.dumps({"message": message})
    ws.send(text_data)
    result =  ws.recv()
    ws.close()


