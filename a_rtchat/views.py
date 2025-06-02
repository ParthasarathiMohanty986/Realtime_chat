# Import necessary Django utilities
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .forms import ChatmessageCreateForm
from django.http import Http404
from .forms import *
from django.contrib import messages
from django.http import HttpResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Import all models from the current app (includes ChatGroup and GroupMessage)
from .models import *

# This decorator ensures only logged-in users can access this view
@login_required
def chat_view(request,chatroom_name='public-chat'):
    """
    This view displays the last 30 messages from the 'public-chat' group.
    Only authenticated users can access this chat page.
    """

    # Try to fetch the chat group with the name "public-chat"
    # If it doesn't exist, return a 404 error page
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)

    other_user=None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user=member
                break
    

    if chat_group.groupchat_name:
        if request.user not in chat_group.members.all():
            # if request.user.emailaddress_set.filter(verified=True).exists():
               chat_group.members.add(request.user)
            # else:
            #     messages.warning(request, 'You need to verify your email to join the chat!')
            #     return redirect('profile-settings')


    # Fetch the latest 30 messages for this group (ordered by newest first due to model's Meta class)
    chat_messages = chat_group.chat_messages.all()[:30]

    form=ChatmessageCreateForm()
    if request.htmx:
        form=ChatmessageCreateForm(request.POST)
        if form.is_valid:
            message=form.save(commit=False)
            message.author=request.user
            message.group=chat_group
            message.save()
            context={
                'message':message,
                'user':request.user
            }
            return render(request,'a_rtchat/partials/chat_message_p.html',context)
        

    context={
        'chat_messages': chat_messages,
        'form':form,
        'other_user': other_user,
        'chatroom_name':chatroom_name,
        'chat_group': chat_group, 
    } 
    

    # Render the template 'a_rtchat/chat.html' and pass the messages to the context
    return render(request, 'a_rtchat/chat.html',context)

@login_required
def get_or_create_chatroom(request, username):
    # Prevent user from creating a chat with themselves
    if request.user.username == username:
        return redirect('home')

    # Get the User object for the other user (the one we want to chat with)
    other_user = User.objects.get(username=username)

    # Get all private chat rooms the current user is part of
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    # Check if any of the current user's private chat rooms include the other user
    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            # Check if the other user is a member of this chatroom
            if other_user in chatroom.members.all():
                # If found, this is the chatroom to use
                chatroom = chatroom
                break  # Exit the loop since we found the chatroom
            else:
                chatroom=ChatGroup.objects.create(is_private=True)
                chatroom.members.add(other_user,request.user)

    else:
        chatroom=ChatGroup.objects.create(is_private=True)
        chatroom.members.add(other_user,request.user)

    return redirect('chatroom',chatroom.group_name)

@login_required
def create_groupchat(request):
    form=NewGroupForm()
    if request.method=='POST':
        form=NewGroupForm(request.POST)
        if form.is_valid():
            new_group  = form.save(commit=False)
            new_group.admin = request.user
            new_group.save()
            new_group.members.add(request.user)
            return redirect("chatroom", new_group.group_name)
    context={
        'form':form,
    }
    return render(request,'a_rtchat/create_groupchat.html',context)


@login_required
def chatroom_edit_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()
    
    form = ChatRoomEditForm(instance=chat_group) 
    
    if request.method == 'POST':
        form = ChatRoomEditForm(request.POST, instance=chat_group)
        if form.is_valid():
            form.save()
            
            remove_members = request.POST.getlist('remove_members')
            for member_id in remove_members:
                member = User.objects.get(id=member_id)
                chat_group.members.remove(member)  
                
            return redirect('chatroom', chatroom_name) 
    
    context = {
        'form' : form,
        'chat_group' : chat_group
    }   
    return render(request, 'a_rtchat/chatroom_edit.html', context) 

@login_required
def chatroom_delete_view(request, chatroom_name):
    context = {}
    chatroom = ChatGroup.objects.get(group_name = chatroom_name)
    
    if request.user != chatroom.admin:
        raise Http404()
    
    if request.method == "POST":
        chatroom.delete()
        messages.success(request, "Chat room Deleted!")
        return redirect("home")   
    
    
    return render(request, "a_rtchat/chatroom_delete.html", {'chat_group':chatroom})


@login_required
def leave_chatroom_view(request, chatroom_name):
    chat_group=get_object_or_404(ChatGroup,group_name=chatroom_name)
    
    if request.user not in chat_group.members.all():
        raise Http404()
    
    # if request.method == 'POST':
    #     chat_group.members.remove(request.user)
    #     messages.success(request, "You left chat.")
    #     return redirect("home")
    
    # return redirect("chatroom", chatroom_name)
    if request.method in ['POST', 'GET']:
        chat_group.members.remove(request.user)
        messages.success(request, "You left chat.")
        return redirect("home")
    
def chat_file_upload(request, chatroom_name):
    chat_group=get_object_or_404(ChatGroup,group_name=chatroom_name)

    if request.htmx and request.FILES:
        file = request.FILES['file']
        message = GroupMessage.objects.create(
            file = file,
            author = request.user,
            group = chat_group,
        )

        channel_layer = get_channel_layer()
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }
        async_to_sync(channel_layer.group_send)(
            chatroom_name, event
        )

    return HttpResponse()
