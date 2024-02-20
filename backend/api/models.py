from django.db import models
from django.contrib.auth.models import User, AbstractUser
from .manager import UserManager

# Create your models here.
import datetime
today = datetime.date.today() #copying dstargram lol

def user_directory_path(instance, filename):
    return 'account/images/{0}/{1}'.format(instance.email, filename)

def media_directory_path(instance, filename):
    return f'media/{today}/{instance.sender.email}/{filename}'

def status_directory_path(instance, filename):
    return f'media/status/{today}/{instance.profile.email}/{filename}'

# class ProfileManager(models.Model):
#     pass

class Profile(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(null=False, max_length=15, unique=True)
    otp = models.CharField(max_length=6, null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    online = models.BooleanField(default=True)
    bio = models.TextField(max_length=125, null=True, blank=True, default='Using whatsclone')
    profile_pic = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        default='account/default.png',
    )
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.email

#add constraint for only 2 participants
class Dm(models.Model):
    participants = models.ManyToManyField(Profile,
                                          symmetrical=False,
                                          through='DmManager')
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
      return f'{self.id}'

class DmManager(models.Model):
    participant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    DM = models.ForeignKey(Dm, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['participant', 'DM'],
                                    name='unique_participants_dm')
        ]
    def __str__(self):
        return f'{self.participant.display_name if self.participant.display_name else self.participant.email} and {self.DM.participants.exclude(email=self.participant.email).get()}: DM {self.DM.id}'

class DmMessage(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='messages')
    message = models.CharField(max_length=255, blank=True)
    edited = models.BooleanField(blank=True, null=True, default=False)
    seen = models.BooleanField(blank=True, null=True, default=False)
    media = models.ImageField(blank=True, null=True, upload_to=media_directory_path)
    DM = models.ForeignKey(Dm,
                           on_delete=models.CASCADE,
                           related_name='messages')
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        other_participant = self.DM.participants.exclude(id=self.sender.id).first()
        return f"{self.sender}: [{self.message[:255]}] in {other_participant}'s dm"
    

class Statu(models.Model): #statu, because django automatically appends an s in admin
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status')
    media = models.FileField(blank=True, upload_to=status_directory_path)
    caption = models.CharField(max_length=100, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile.display_name} posting {self.caption if self.caption else "a video"}'


class SvelteMessages(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)