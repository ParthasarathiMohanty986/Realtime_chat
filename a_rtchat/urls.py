from django.urls import path
from .views import *

urlpatterns=[
    path('',chat_view,name="home"),
    path('chat/<username>',get_or_create_chatroom,name="start-chat"),
    path('chat/room/<chatroom_name>',chat_view,name="chatroom"),
    path('chat/new_groupchat/',create_groupchat,name="new-groupchat"),
    path('chat/edit/<chatroom_name>',chatroom_edit_view,name="edit-chatroom"),
    path('chat/delete/<chatroom_name>',chatroom_delete_view,name="delete-chatroom"),
    path('chat/leave/<chatroom_name>',leave_chatroom_view,name="leave-chatroom"),
    path('chat/file_upload/<chatroom_name>',chat_file_upload,name="chat-file-upload"),
]