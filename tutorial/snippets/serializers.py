from rest_framework import serializers
from snippets.models import Twitter
from twitter import twitterScript
class TwitterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Twitter
        fields = ['author_id','tweet_id','tweet','created_at','author_name','author_username','url_to_tweet']


