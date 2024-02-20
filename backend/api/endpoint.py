from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .serializers import *
from api.models import *
from api.emails import send_otp_email

from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

# Create your views here.

@api_view(['POST'])
def register_user(request):
    try:
        data = request.data
        serializer = CreateProfileSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            serializer = ProfileSerializer(instance=user)
            try:
                send_otp_email(serializer.data['email'])
                print('email sent')
            except Exception as e:
                print(e, 'this is the exception') #reminder to try and implement a more error specific check
                Profile.objects.get(email=serializer.data['email']).delete() #so I won't do it manually
                return Response({'status':400, 'error':{'Could not send email'}})
            return Response({'status':200})
        else:
            return Response({'status':400, 
                             'error':serializer.errors})
    except Exception as e:
        print(e)
    
    

@api_view(['POST'])
def otp_verification(request):
    data = request.data
    serializer = VerifyEmailSerializer(data=data)

    if serializer.is_valid():
        email = serializer.data['email']
        otp = serializer.data['otp']

        user = Profile.objects.get(email=email)
        if not user:
            return Response({
                'status':400,
                'message':'invalid user',
                'error':serializer.errors
            })
        if user.otp != otp:
            return Response({
                'status':400,
                'message':'invalid otp code. Please check you typed the correct code',
                'error':serializer.errors
            })
        user.is_verified = True
        user.otp = ''
        user.save()
        serializer = ProfileSerializer(instance=user)
        data = serializer.data
        data['is_verified'] = True
        return Response({
            'status':200,
            'message':'account verified',
            'data':data
        })