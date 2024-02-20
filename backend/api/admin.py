from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Dm)
admin.site.register(DmManager)
admin.site.register(DmMessage)
admin.site.register(SvelteMessages) #depreciated
admin.site.register(Statu)