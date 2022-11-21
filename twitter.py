import json
import os
import pandas as pd
import requests
import time
import asyncio
import websockets

file = open("BearerToken.txt",'r')

os.environ['TOKEN'] =  file.read()
def auth():
    return os.getenv('TOKEN')

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

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

def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def connect_to_endpoint2(url, headers):
    params = {}
    params['tweet.fields'] ='text' 
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def give_the_data(data):
    url = 'http://0.0.0.0:8000/twitter/'
    for obj in data:
        x = requests.post(url, json=obj)
        if x.status_code !=201:
            raise Exception(x.status_code, x.text)
    
def connect_to_endpoint3 ():
    params = {'tweet_id'}
    url = 'http://0.0.0.0:8000/twitter/'
    response = requests.request("GET", url)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
async def produce(message: str, host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}") as ws:
        await ws.send(message)
        print("> {}".format(message))
        response = await ws.recv()
        print("< {}".format(response))


bearer_token = auth()
headers = create_headers(bearer_token)
keyword = "#Love"
max_results = 10
url = create_url (keyword,max_results)

json_response = connect_to_endpoint(url[0], headers, url[1])
test = json.dumps(json_response, indent = 4, sort_keys = True)

json_response3 = connect_to_endpoint3()
duplicates = []
for a in json_response3:
    duplicates.append(a['tweet_id'])

solution =  []
print("Solutions for: " + keyword)
for i in range(0,len(json_response['data'])):
    if int(json_response['data'][i]['id']) in duplicates:
        print('duplicate:' + str(json_response['data'][i]['id']))
    else:
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
if (len(duplicates) - len(solution) > 0):
    #funckija za brisanje zadnjih dodanih podataka
    pass

give_the_data(solution)