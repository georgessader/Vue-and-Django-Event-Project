from django.db import models
from django.contrib.auth.models import User

class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_title = models.CharField(max_length=200,null=False,blank=False)
    event_date = models.DateTimeField()
    event_status = models.CharField(max_length=200,null=False,blank=False)
    event_location = models.CharField(max_length=200,null=False,blank=False)

class EventsOwner(models.Model):
    event_id = models.ForeignKey(Events, to_field="event_id", on_delete=models.CASCADE)
    username = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE)

class SubscribeEvent(models.Model):
    event_id = models.ForeignKey(Events, to_field="event_id", on_delete=models.CASCADE)
    username = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE)

class SuperUsers(models.Model):
    username = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE)