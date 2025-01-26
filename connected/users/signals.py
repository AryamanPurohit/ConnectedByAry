from django.db.models.signals import post_save, post_delete
from .models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail
#Since we have a 1-1 reln between User and Profile, we need that as soon as a user is created it's profile should also be created.
#Signals are used in such case scenarios.

def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,

        )
        send_mail(
                "Welcome To Connected- By Aryaman Purohit",
                "We are glad that you chose Connected to expand your network!",
                "connectedbyaryaman@gmail.com",
                [profile.email],
                fail_silently=False,
                )   


    
def userDeleted(sender,instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass

def updateUser(sender, instance, created,**kwargs ):
    profile = instance

    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


post_save.connect(createProfile, sender = User)  #(kya karna he, kis model ke save hone par krna he)
post_save.connect(updateUser, sender = Profile)  #ASAP PROFILE is updated the user will also get updated
post_delete.connect(userDeleted, sender = Profile)