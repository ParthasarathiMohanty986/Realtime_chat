from django.db import models
from django.contrib.auth.models import User
import shortuuid
#from PIL import Image
# Create your models here.
class ChatGroup(models.Model):
    group_name=models.CharField(max_length=128,unique=True,default=shortuuid.uuid)
    groupchat_name=models.CharField(max_length=128,null=True,blank=True)
    admin=models.ForeignKey(User,related_name='groupchats',null=True,blank=True,on_delete=models.SET_NULL)
    users_online = models.ManyToManyField(User,related_name='online_in_groups',blank=True)
    members=models.ManyToManyField(User,related_name='chat_groups',blank=True)
    is_private=models.BooleanField(default=False)

    def __str__(self):
        return self.group_name

class GroupMessage(models.Model):
    body=models.CharField(max_length=300,blank=True,null=True)
    file=models.FileField(upload_to='files/',blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    group=models.ForeignKey(ChatGroup,related_name='chat_messages',on_delete=models.CASCADE)
    author=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        if self.body:
           return f'{self.author.username}:{self.body}'
        elif self.file:
            return f'{self.author.username}:{self.file}'

    
    class Meta:
        ordering=['-created']

          
    @property    
    def is_image(self):
        if self.file.name.lower().endswith(('.jpg','.png','.jpeg','.svg')):
            return True
        else:
            return False
        
        
      