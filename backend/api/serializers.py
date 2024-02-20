from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from api.models import *

class CreateProfileSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    class Meta:
        model = Profile
        fields = ['id','email', 'password', 'phone','is_verified']
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(CreateProfileSerializer, self).create(validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    last_login = serializers.SerializerMethodField()
    def get_last_login(self, obj):
        return obj.last_login if obj.last_login else obj.date_joined

    class Meta:
        model = Profile
        fields = ['id','email', 'phone','profile_pic','bio','display_name', 'online', 'last_login']

class DmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dm
        fields = '__all__'


from django.contrib.staticfiles.storage import staticfiles_storage
class DMMessageSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()   

    profile_pic = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()

    def get_profile_pic(self, obj):
        return obj.sender.profile_pic.url if obj.sender.profile_pic else None

    def get_profile(self, obj):
        return obj.sender.email
    
    def get_media(self, obj):
        return staticfiles_storage.url(obj.media.url) if obj.media else None
    
    class Meta:
        model = DmMessage
        fields = ('message', 'profile_pic', 'profile', 'sender', 'date', 'media', 'seen')

class CreateDMMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DmMessage
        fields = ('message', 'media',)

class StatusSerializer(serializers.ModelSerializer): #been sweating for the past how many frickin minutes. Wondering why the statuses weren't serializing till I came here and realized it wasn't '.Modelserializer' :facepalm:
    profile = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()
    display = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()

    def get_media(self, obj):
        return staticfiles_storage.url(obj.media.url) if obj.media else None
    def get_profile(self, obj):
        return obj.profile.email
    def get_display(self, obj):
        return obj.profile.display_name if obj.profile.display_name else obj.profile.phone
    def get_profile_pic(self, obj):
        return obj.profile.profile_pic.url
    class Meta:
        model = Statu
        fields = ['profile', 'display', 'profile_pic', 'caption', 'media', 'time']

class CreateStatusPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statu
        fields = ['caption', 'media']

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

#legacy code from when I started lol
class SvelteMessageSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    profile_pic =serializers.SerializerMethodField()

    def get_profile_pic(self, obj):
        print(obj.sender.profile_pic)
        return obj.sender.profile_pic.url if obj.sender.profile_pic else None

    def get_profile(self, obj):
        return obj.sender.user.username
    
    class Meta:
        model = SvelteMessages
        fields = ['sender', 'message', 'profile', 'date', 'profile_pic']

# class CreateSvelteMessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SvelteMessages
#         fields = ('message',) Those days of testing lol