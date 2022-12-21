import tweepy
from snippets.models import Twitter
import json
from websocket import create_connection
# My TOP SECRET_KEY to connect on twitter
bearer_token = "AAAAAAAAAAAAAAAAAAAAAKM9jQEAAAAAdS9J7AcLHZ0IlHg3bRlERKwW2fU%3DtiqFpEiBqMRimDuKgdrm41BjwpUweyxjnxSRhZG6qjblaklZp5"
# authentication for twitter
client = tweepy.Client(bearer_token)

# Using tweepy searching recent tweets (max_results is default 10) with given parametars


def getTweets(hashtag):
    return client.search_recent_tweets(hashtag, tweet_fields='id,text,author_id,created_at', expansions=['author_id'])

# From json format to nice list with dictionaries with it
# [{author_id,tweet_id,tweet, created_at, author_name, author_username, url}]


def formatTweets(response):
    solution = []
    for tweet in response.data:
        for check in response.includes['users']:
            if check['id'] == tweet['author_id']:
                author_name = check['name']
                author_username = check['username']
        solution.append({
            'author_id': tweet['author_id'],
            'tweet_id': tweet['id'],
            'tweet': tweet['text'],
            'created_at': tweet['created_at'],
            'author_name': author_name,
            'author_username': author_username,
            'url': 'twitter.com/' + str(tweet['author_id']) + '/status/' + str(tweet['id'])
        })
    return solution

# Going to database using Twitter model to retrive 10 latest tweet that i have saved


def getLatest():
    data = Twitter.objects.values_list()
    latest = []
    for i in data:
        latest.append(i[1])
    return latest

# Deleting from database using Twitter model to remove unnecessary tweets(they are older than 10 latest)


def deleteLatest(solution, latest):
    # Getting list of tweet_ids that i have gathered from latest tweet
    list_of_keys = []
    for tweet_info in solution:
        list_of_keys.append(tweet_info['tweet_id'])
    # If there is no matching tweet id from database to newly created list, delele from database
    for tweet_id2 in latest:
        if tweet_id2 not in list_of_keys:
            Twitter.objects.get(tweet_id=tweet_id2).delete()

# Removing copies if there is any, Checking from database to newly scraped tweets and if there is matching tweet id it removes it from solutions


def removeCopies(solution, latest):
    for tweet_id in latest:
        for j in range(0, len(solution)):
            try:
                if str(solution[j]['tweet_id']) == str(tweet_id):
                    solution.pop(j)
                    break
            except ValueError:
                pass
    return solution

# Writing in database using Twitter model


def writeInDB(solution):
    for data in solution:
        t = Twitter.objects.create(author_id=data['author_id'], tweet_id=data['tweet_id'], tweet=data['tweet'], created_at=data['created_at'],
                                   author_name=data['author_name'], author_username=data['author_username'], url_to_tweet=data['url']),

# Send only new data to websocket


def send_to_ws(tweet_information, ws):
    text_data = json.dumps({"message": tweet_information})
    ws.send(text_data)


def run(hashtag='croatia'):
    hashtag2 = '#' + hashtag
    response = getTweets(hashtag2)
    solutions = formatTweets(response)
    latest = getLatest()
    deleteLatest(solutions, latest)
    solutions = removeCopies(solutions, latest)
    writeInDB(solutions)
    url_for_ws = "ws://127.0.0.0:8000/ws/chat/" + hashtag + "/"
    ws = create_connection(url_for_ws)
    for i in solutions:
        # Formating beacuse json dind't like it the way tweepy has done it
        i['created_at'] = i['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        send_to_ws(i, ws)
    ws.close()
    print("Successfuly sent", len(solutions), "solutions")


if __name__ == '__main__':
    run('#Fifa')
