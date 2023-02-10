from rest_framework import routers,serializers,viewsets
from django.contrib.auth.models import User
from .models import Events,SubscribeEvent,SuperUsers

class EventsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Events
        fields = ['event_id','event_title', 'event_date', 'event_status','event_location']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'username']

class SubscribeSerialize(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubscribeEvent
        fields = ['event_id','username']

class SuperUsersSerialize(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SuperUsers
        fields = ['username']