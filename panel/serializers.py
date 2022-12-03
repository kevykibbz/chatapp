from rest_framework import serializers
from .models import *
from django.contrib.auth.forms import User


class CommentSerializers(serializers.ModelSerializer):
	class Meta:
		model=CommentModel
		fields='__all__'

class TweetSerlializer(serializers.ModelSerializer):
	class Meta:
		model=TweetModel
		fields=('message','likes_count','retweet_count','tweet_image','comment_count',)

class UserSerlializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields=('username','first_name','last_name','id','email',)

class ChatSerializer(serializers.ModelSerializer):
	class Meta:
		model=ChatModel
		fields='__all__'