from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout

from .serializers import *
from api.models import *

##
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.
@api_view(['GET'])
def index(request):
    context = {
        'list of url routes': '/index',
    }
    return Response(context)

from django.shortcuts import get_object_or_404

@api_view(['POST'])
def message(request):
    data = request.data
    user = Profile.objects.get(email=data['user'])
    # participant = Profile.objects.get(email=data['participant'])
    try:
        DM = Dm.objects.filter(participants = user).filter(participants__email=data['participant']).get()
        #print(DM)
    except Dm.DoesNotExist:
        DM = Dm.objects.create()
        DM.participants.add(user)
        dm_profile = get_object_or_404(Profile, email=data['participant'])
        DM.participants.add(dm_profile.id)
    except Dm.MultipleObjectsReturned as e:
        return Response({'error':'pokk'})
    dm_messages = DM.messages.order_by('date')
    # serializer = DmSerializer(DM, many=False)
    serializer_messages = DMMessageSerializer(dm_messages, many=True)

    return Response(serializer_messages.data)


@api_view(['POST'])
def contactlist(request):
    data = request.data
    user = Profile.objects.get(email=data['user'])
    contactlist = []
    try:
        contacts = Dm.objects.filter(participants=user)
        #print(contacts)
        for i in contacts:
            profile = i.participants.exclude(email=data['user'])[0]
            serializer = ProfileSerializer(profile)
            last_message = DMMessageSerializer(i.messages.last())
            new_dict = {'Dm_id':i.id, 'index':last_message.data['date']}
            new_dict.update(serializer.data)
            contactlist.append(new_dict)
        #print(contactlist)
        
        return Response(contactlist)
    except Exception as e:
        print(e)
        return JsonResponse({'error':'error shaa'})

@api_view(['POST'])
def newcontactlist(request): #reading on 10/8/23 - all profiles looking scary tho
    data = request.data
    user = Profile.objects.get(email=data["user"])
    blacklist = ['emmanueladesipe@gmail.com'] #id of profiles that the person already has dms with
    contactlist = []
    try:
        contacts = Dm.objects.filter(participants=user)
        blacklist.append(user.email) #the user themself
        for i in contacts:
            profile = i.participants.exclude(email=data['user'])[0]
            blacklist.append(profile.email)
        profiles = Profile.objects.exclude(email__in=blacklist) #filtering out profiles in the blacklist
        for i in profiles:
            serializer = ProfileSerializer(i)
            # serializer.data.__delitem__('last_login')
            new_dict = {'date_joined':i.date_joined}
            new_dict.update(serializer.data)
            new_dict.__delitem__('last_login')
            contactlist.append(new_dict)
        return Response(contactlist)
    except Exception as e:
        print(e)
        return Response({'error':'error shaaaaa'})
#user stuff
    
from collections import defaultdict
@api_view(['POST'])
def status(request):
    data = request.data
    user = Profile.objects.get(email=data['user'])
    status_posts = []
    contacts = Dm.objects.filter(participants=user)
    for i in contacts:
        profile = i.participants.exclude(email=data['user'])[0]
        status = profile.status.order_by('time')
        if status:
            status_posts.append(status) #retrieves the status data

    status = []
    for j in status_posts:
        serializer = StatusSerializer(j, many=True) #have to iterate the queryset in the list
        for k in serializer.data:
            status.append(k) #serializes the status data

    orderedStatus = defaultdict(list)

    for i in status:
        profile = i['profile']
        orderedStatus[profile].append(i) #maps each status dict to the user
    
    Status = dict(orderedStatus)
    last_list = []
    for profile in Status:
        post_dict = {'profile':profile}
        post_dict['posts'] = Status[profile]
        last_list.append(post_dict)
    return Response(last_list)

@api_view(['POST'])
def user_status(request):
    data = request.data
    user = Profile.objects.get(email=data['user'])
    status_posts = user.status
    serializer = StatusSerializer(status_posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def get_user(request):
    data = request.data
    user = Profile.objects.get(email=data['user'])
    message = DmMessage.objects.filter(DM__participants=user).get(date=data['message'])
    print(message)
    # message = DmMessage.objects.get(id=1)
    serializer = ProfileSerializer(user)
    new_dict = {'Dm_id':message.DM.id, 'index':message.date} #improvised using the latest message from user to get relevant dm info. (10/8-you smart monkey)
    new_dict.update(serializer.data)
    return Response (new_dict)

@api_view(['POST'])
def update_profilepic(request):
    profile_pic = request.data.get('profile_pic')
    parser_classes = [MultiPartParser]
    data = request.data
    print(data)
    user = Profile.objects.get(email=data['email'])
    user.profile_pic = profile_pic
    user.save()
    serializer = ProfileSerializer(instance=user)
    #print(serializer.data['profile_pic'])
    return JsonResponse({'status':200, 
                         'profile_pic':staticfiles_storage.url(serializer.data['profile_pic'])}) #nice work man


@api_view(['POST'])
def update_username(request):
    data = request.data
    info = data['info']
    user = Profile.objects.get(email=data['email'])
    user.display_name = info
    user.save()
    return JsonResponse({'status':200})

@api_view(['POST'])
def update_userbio(request):
    data = request.data
    info = data['info']
    user = Profile.objects.get(email=data['email'])
    user.bio = info
    user.save()
    return JsonResponse({'status':200})


from django.utils import timezone
@api_view(['POST'])
def offline(request):
    data = request.data
    user = Profile.objects.get(email=data['email'])
    user.last_login = timezone.now()
    user.online = False
    user.save()
    return JsonResponse({'last_login':user.last_login})

@api_view(['POST'])
def online(request):
    data = request.data
    user = Profile.objects.get(email=data['email'])
    user.online = True
    user.save()
    return JsonResponse({'online':True})

@api_view(['POST'])
def last_login(request):
    data = request.data
    user = Profile.objects.get(email=data['email'])
    return JsonResponse({'last_login':user.last_login})


@api_view(["POST"])
def createmessage(request):
    data = request.data
    parser_classes = [MultiPartParser]
    #print(data)
    user_profile = Profile.objects.get(email=data['email'])
    participant = Profile.objects.get(email=data['participant'])
    try:
        DM = Dm.objects.filter(participants=user_profile).filter(participants=participant).get()
    except Dm.DoesNotExist:
        DM = Dm.objects.create()
        DM.participants.add(user_profile)
        DM.participants.add(participant)
    form_serializer = CreateDMMessageSerializer(data=data)
    if form_serializer.is_valid():
        message = form_serializer.save(sender=user_profile, DM=DM)
        serializer = DMMessageSerializer(instance=message)
        return Response(serializer.data, status=201)
    return Response(form_serializer.errors, status=400)

@api_view(['POST'])
def createpost(request):
    data = request.data
    user = Profile.objects.get(email=data['email'])
    form_serializer = CreateStatusPostSerializer(data=data)
    if form_serializer.is_valid():
        post = form_serializer.save(profile=user)
        serializer = StatusSerializer(instance=post)
        return Response(serializer.data, status=201)
    return Response(form_serializer.error, status=400)

def deletepost(request):
    data = request.data
    user = Profile.objects.get(email=data['email'])
    status = Statu.objects.filter(profile = user).filter(time=data['time'])
    status.delete
#modify contactlist to return {latestmessage; display_name, phone, email; latest_message; last date 
# and number of unreads to be done at frontend}

from django.contrib.staticfiles.storage import staticfiles_storage

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['phone'] = user.phone
        token['email'] = user.email
        token['display'] = user.display_name
        token['is_verified'] = user.is_verified
        token['bio'] = user.bio
        #token['last_login'] = user.last_login not needed lol
        if user.profile_pic:
            # # Get the URL of the profile pic
            profile_pic_url = user.profile_pic.url if user.profile_pic else None
            # If the profile pic is served through Django's static files, use staticfiles_storage
            profile_pic_url = staticfiles_storage.url(profile_pic_url)

            token['profile_pic'] = profile_pic_url
        # ...

        
        return token
        
        
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer