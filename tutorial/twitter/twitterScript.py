#Imports:
import json
import os
import requests
from websocket import create_connection
import time
import sys


#Creating twitter url for GET reqeuest method
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

#Gathering data from twitter for multiple tweets throufgh url,headers, and params
def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token
    response = requests.request("GET", url, headers = headers, params = params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

#Gathering tweet field if tweet filed from searching multiple tweets hase over 230 characters
def connect_to_endpoint2(id_of_tweet, headers):
    url = 'https://api.twitter.com/2/tweets/' + id_of_tweet
    params = {'tweet.fields':'text'}
    response = requests.request("GET", url, headers = headers, params = params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

#Reading the collected data and writing is to a list
#solutions with dict atribute
#soluition = [{mmessage, author_id, tweet_id, created_at, author_name, author_username, tweet_url}]
def create_solution(json_response, headers):
    try:
        solution = []
        for i in range(0,len(json_response['data'])):

            if len(json_response['data'][i]['text']) > 230:
                json_response2 =connect_to_endpoint2(str(json_response['data'][i]['id']),headers)
                message = json_response2['data']['text']
            else:
                message = json_response['data'][i]['text']
                
            author_id = json_response['data'][i]['author_id']
            tweet_id = json_response['data'][i]['id']
            created_at = json_response['data'][i]['created_at']
            for user in json_response['includes']['users']:
                if(author_id == user['id']):
                    author_name = user['name']
                    author_username = user['username']
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
    except KeyError:
        print('There is not any new data given at the moment')    
    return solution

#Getting data from server 
def connect_to_endpoint3 (url):
    print('koenkcije ide ' + url)
    response = requests.get(url)
    print('prosao')
    print(response)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def create_duplicates(url):
    print('usao')
    json_response3 = connect_to_endpoint3(url) 
    print('konektovao sam se')
    duplicates = []
    print(duplicates)
    for tweet in json_response3:
        duplicates.append(tweet['tweet_id'])
    return duplicates

#Deleting tweets which are older than collected tweets
def delete_tweets(solution, duplicates, url):
    print('usao u delte tweet')
    list_of_keys=[]
   
    for tweet_info in solution:
        
        list_of_keys.append(tweet_info['tweet_id'])
   
    for tweet_id in duplicates:

        if str(tweet_id ) not in list_of_keys:
            print('saljem request')
            requests.delete(url + str(tweet_id))

#Removing unneceseary duplicates
def remove_duplicates(duplicates,solution):
    for tweet_id in duplicates:
        for j in range(0,len(solution)):
            try:
                if str(solution[j]['tweet_id']) == str(tweet_id):
                    solution.pop(j)
                    break
            except ValueError:
                pass
    return solution

#Uploading data on server via POST request
def give_the_data(solution, url):
    for obj in solution:
        x = requests.post(url, json=obj)
        if x.status_code !=201:
            raise Exception(x.status_code, x.text)

#Sending tweets to WebSocket
def send_to_ws(tweet_information,ws):
    text_data=json.dumps({"message": tweet_information})
    ws.send(text_data)


def authorization():
    file = open("/home/antonio/DBSQLDjango/tutorial/twitter/BearerToken.txt",'r')
    os.environ['TOKEN'] =  file.read()
    bearer_token = os.getenv('TOKEN')
    return {"Authorization": "Bearer {}".format(bearer_token)}

#MAIN
if __name__ == '__main__':
    print('usao')

    time.sleep(2)
    headers = authorization()
    keyword = '#' + str(sys.argv[1])
    max_results = 10
    url_tweet = create_url (keyword,max_results)
    url_for_ws ="ws://127.0.0.0:8000/ws/chat/" + str(sys.argv[1]) + "/"
    url = 'http://127.0.0.0:8000/twitter/'
    print(url_for_ws)
    ws =create_connection(url_for_ws)
    while True:
        try:
            json_response = connect_to_endpoint(url_tweet[0], headers, url_tweet[1])    
            solution=create_solution(json_response, headers)
            print('Nakon soluztiona:')
            duplicates=create_duplicates(url)
            delete_tweets(solution,duplicates,url)
            solution = remove_duplicates(duplicates,solution)
            give_the_data(solution, url)
            for i in solution:
                send_to_ws(i, ws)
            time.sleep(10)
        except KeyboardInterrupt:
            break
    ws.close()
