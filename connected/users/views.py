from django.shortcuts import render,redirect
from .models import Profile,Skill,Message
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from .utils import searchProfiles, paginateProfiles

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method =='POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username =username)
        except:
            messages.error(request, "Username Doesn't exist!")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request,"Successfully Logged In!")
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, "USERNAME OR PASSWORD IS INCORRECT!")
            

    return render(request, 'users/login_reg.html')

def logoutPage(request):
    logout(request)
    messages.error(request, "USER SUCCESSFULLY LOGGED OUT!")
    return redirect('login')



def registerUser(request):
    page ='register'

    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User Registered!')

            login(request, user)
            return redirect('edit-account')
        else:
            messages.success(request, 'Error Occured!')


    context = {'page':page, 'form':form}
    return render(request, 'users/login_reg.html', context)

def profiles(request):

    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 3)
    
    context = {'profiles' : profiles, 'search_query':search_query, 'custom_range':custom_range}
    return render(request,'users/profiles.html',context)

def userProfile(request,pk):

    profile = Profile.objects.get(id=pk)
    topSkills= profile.skill_set.exclude(description="")
    otherSkills = profile.skill_set.filter(description="")
    

    return render(request, 'users/user-profile.html', {'profile' : profile, 'topSkills':topSkills,'otherSkills':otherSkills})


@login_required(login_url='login')
def userAccount(request):

    profile = request.user.profile

    topSkills= profile.skill_set.all()
    projects = profile.project_set.all()


    context={'profile':profile, 'topSkills':topSkills, 'projects':projects}
    return render(request,'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context={'form':form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def addSkill(request):

    profile = request.user.profile
    form = SkillForm()

    if request.method =='POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()

            return redirect('account')

    context={'form':form}
    return render(request,'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):

    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)    # 1 to N reln between Profile and Skill models
    form = SkillForm(instance = skill)

    if request.method =='POST':
        form = SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()

            return redirect('account')

    context={'form':form}
    return render(request,'users/skill_form.html', context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        return redirect('account')

    return render(request, 'delete_temp.html',{'object': skill})

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageSet = profile.messages.all()     # messages here is the related name in recepient field in Message Model
    unreadCount = messageSet.filter(is_read =False).count()
    return render(request,'users/inbox.html',{'messageSet':messageSet, 'unreadCount':unreadCount})

@login_required(login_url='login')
def viewMessage(request,pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)

    if message.is_read == False:
        message.is_read = True
        message.save()
    return render(request, 'users/message.html',{'message':message})

def sendMessage(request,pk):
    form =MessageForm()
    recipient = Profile.objects.get(id=pk)

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recepient = recipient
            
            message.save()

            messages.success(request,"Message Succesfully Sent!")
            return redirect('user-profile', pk=recipient.id)

    return render(request, 'message_form.html', {'form':form,'rec':recipient})