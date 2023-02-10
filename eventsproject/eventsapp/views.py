from django.shortcuts import render,redirect
from .forms import signupform
from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session
from .models import Events,EventsOwner,SubscribeEvent, SuperUsers
from django.contrib.auth.models import User
from django.db import connection

from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .serializers import EventsSerializer,UserSerializer,SuperUsersSerialize

@csrf_exempt
def signUpRequest(request):
    try:
        if request.method=='POST':
            form = signupform(request.POST)
            if form.is_valid():
                form.save()
                d = User.objects.get(username=request.POST.get("username"))
                d.first_name = request.POST.get("first_name")
                d.last_name = request.POST.get("last_name")
                d.email = request.POST.get("email")
                d.save()
                return HttpResponse("Success")
            else:
                return HttpResponse("Error Registering")
        else:
            form = signupform()
    except:
        return HttpResponse("Error Registering")

@csrf_exempt
def loginRequest(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            request.session['username'] = username
            return HttpResponse("Success")
    return HttpResponse("Username or password incorrect")

@csrf_exempt
def createEvent(request):
    if request.method == 'POST':
        list_of_errors=[]
        statusList=["Draft","Private","Public"]
        title = request.POST.get('eventTitle')
        date = request.POST.get('eventDate')
        status = request.POST.get('eventStatus')
        location = request.POST.get('eventLocation')
        usernameReq = request.POST.get('username')
        list_of_errors.append("Missing: ")
        if title=="":
            list_of_errors.append("Title ")
        if date=="":
            list_of_errors.append("Date ")
        if status=="" or status not in statusList:
            list_of_errors.append("Status ")
        if location=="":
            list_of_errors.append("Location ")
        if len(list_of_errors)>1:
            return HttpResponse(list_of_errors)
        else:
            try:
                d = Events(
                event_title=title,
                event_date=date,
                event_status=status,
                event_location=location)
                d.save()

                u=User.objects.get(username=usernameReq)
                d1 = EventsOwner(
                    event_id=d,
                    username=u)
                d1.save()
                return HttpResponse("Success")
            except:
                return HttpResponse("Error inserting event")

@csrf_exempt
def getMyEvents(request):
    if request.method == 'POST':
        owner = EventsOwner.objects.filter(username=request.POST.get('username'))
        myevent = Events.objects.filter(eventsowner__in=list(owner))
        users = User.objects.filter(eventsowner__in=list(owner))
        s=[EventsSerializer(myevent, many=True).data,UserSerializer(users, many=True).data]
        return JsonResponse(s,safe=False)

@csrf_exempt
def editMyEvent(request):
    if request.method == 'POST':
        try:
            d = Events.objects.get(event_id=request.POST.get("eventId"))
            d.event_title = request.POST.get("eventTitle")
            d.event_date = request.POST.get("eventDate")
            d.event_location = request.POST.get("eventLocation")
            d.event_status = request.POST.get("eventStatus")
            d.save()
            return HttpResponse("Event edited Successfully")
        except:
            return HttpResponse("Error editing event")


@csrf_exempt
def deleteMyEvent(request):
    if request.method == 'POST':
        try:
            Events.objects.filter(event_id=request.POST.get("eventId")).delete()
            EventsOwner.objects.filter(event_id=request.POST.get("eventId"),username=request.POST.get("username")).delete()
            return HttpResponse("Student deleted Successfully")
        except:
            return HttpResponse("Error deleting student")


@csrf_exempt
def getEvents(request):
    if request.method == 'POST':
        # owner = EventsOwner.objects.exclude(username=request.POST.get('username'))
        owner = EventsOwner.objects.all()
        myeventsowner = EventsOwner.objects.filter(username=request.POST.get('username'))
        
        isSuper=0

        if(request.POST.get('isSearch')=="true"):
            # I choosed to send the fileds data as dictionary to control the dynamic of search
            # which means in case client want to search only in title and location it will ignore 
            # the other field by removing them from the dictionary
            d={
                'event_title':request.POST.get('eventTitle'),
                'event_status__in':list(request.POST.get('eventStatus').split(",")),
                'event_date__startswith':request.POST.get('eventDate'),
                'event_location':request.POST.get('eventLocation')
            }
            # d.update(extra)
            lastd={}
            for k,v in d.items():
                if v!="":
                    lastd[k]=v

            if lastd["event_status__in"][0]=='':
                del lastd["event_status__in"]

            if(request.POST.get('username')!="null"):
                lastd['eventsowner__in']=list(owner)
                event = Events.objects.filter(**lastd).exclude(event_status="Draft")
                lastd['eventsowner__in']=list(myeventsowner)
                myevent2=Events.objects.filter(**lastd)
                event=event.union(myevent2)
                isSuper = SuperUsers.objects.filter(username=request.POST.get('username')).count()
            else:
                event = Events.objects.filter(**lastd).exclude(event_status__in=["Private","Draft"])
        else:
            if(request.POST.get('username')!="null"):
                event = Events.objects.filter(eventsowner__in=list(owner)).exclude(event_status="Draft") 
                myevent2=Events.objects.filter(eventsowner__in=list(myeventsowner))  
                event=event.union(myevent2)
                isSuper = SuperUsers.objects.filter(username=request.POST.get('username')).count()
            else:  
                event = Events.objects.filter(eventsowner__in=list(owner)).exclude(event_status__in=["Private","Draft"])
    
        # users = User.objects.filter(eventsowner__in=list(owner))

        o = SubscribeEvent.objects.filter(username=request.POST.get('username'))
        subs = Events.objects.filter(subscribeevent__in=list(o))


        d={}
        u={}
        for s in event:
            d[s.event_id]=SubscribeEvent.objects.filter(event_id=s.event_id).count()
            owner = EventsOwner.objects.filter(event_id=s.event_id)
            u[s.event_id]=UserSerializer(User.objects.filter(eventsowner__in=list(owner)), many=True).data

        s=[EventsSerializer(event, many=True).data,u,EventsSerializer(subs, many=True).data,d,isSuper]
        return JsonResponse(s,safe=False)



@csrf_exempt
def subscribeEvent(request):
    if request.method == 'POST':
        id = request.POST.get('eventId')
        username = request.POST.get('username')
        try:
            idevent=Events.objects.get(event_id=id)
            uevent=User.objects.get(username=username)
            d1 = SubscribeEvent(
                event_id=idevent,
                username=uevent)
            d1.save()
            return HttpResponse("Success")
        except:
            return HttpResponse("Error inserting event")


@csrf_exempt
def unSubscribeEvent(request):
    if request.method == 'POST':
        id = request.POST.get('eventId')
        username = request.POST.get('username')
        try:
            SubscribeEvent.objects.filter(event_id=id,username=username).delete()
            return HttpResponse("Success")
        except:
            return HttpResponse("Error inserting event")


@csrf_exempt
def getSubscribers(request):
    if request.method == 'POST':
        o = SubscribeEvent.objects.filter(event_id=request.POST.get('eventId'))
        users = User.objects.filter(subscribeevent__in=list(o))
        s=UserSerializer(users, many=True).data
        return JsonResponse(s,safe=False)


