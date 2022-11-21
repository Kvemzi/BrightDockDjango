from rest_framework import serializers
from snippets.models import LANGUAGE_CHOICES, STYLE_CHOICES, Snippet, Twitter


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']
class TwitterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Twitter
        fields = ['author_id','tweet_id','tweet','created_at','author_name','author_username','url_to_tweet']