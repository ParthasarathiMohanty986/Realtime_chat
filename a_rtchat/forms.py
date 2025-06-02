from django import forms
from django.forms import ModelForm
from .models import *

class ChatmessageCreateForm(ModelForm):
    class Meta:
        model=GroupMessage
        fields=['body']
        widgets={
            'body':forms.TextInput(attrs={'placeholder':'Add message...','class':'p-4 text-black','max-length':300,'autofocus':True}),
        }

class NewGroupForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ["groupchat_name"]
        widget = {
            "groupchat_name": {
                forms.TextInput(attrs={
                    "placeholder": "Add Name...",
                    "class": "p-4 text-black",
                    "maxlength": 300,
                    "autofocus": True
                })
            }
        }


class ChatRoomEditForm(forms.ModelForm):
    
    class Meta:
        model = ChatGroup
        fields = ['groupchat_name']
        widget = {
            'groupchat_name':{
                forms.TextInput(attrs={
                    "class": "p-4 text-xl font-bold mb-4",
                    "maxlength": 300                    
                })
            }
        }
