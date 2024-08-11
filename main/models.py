from django.db import models
from django.contrib.auth import get_user_model
from account.models import Profile
import uuid ,datetime

# Create your models here
# Create your models here.





class Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="posts",blank=False,null =False)
    caption = models.CharField(max_length=1000)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    likes = models.IntegerField(default=0,blank=False,null=False)
    no_comments = models.IntegerField(default=0,blank=False,null=False)
    
    
    def __str__(self):
        return str(self.id)

    
class Like(models.Model):
    postid = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    def __str__(self):
        return self.username

class Comment(models.Model):
    postid = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    def __str__(self):
        return '{0} , {1}'.format(self.profile.user.username,self.postid)


class Relation(models.Model):
    relatedpost = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="postr")
    relatedcom = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="commentr")
    def __str__(self):
        return '{0} , {1}'.format(self.relatedcom.profile.user.username,self.relatedpost.id)


class Follow(models.Model):
    User = get_user_model()
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name="follower")
    followed = models.ForeignKey(User,on_delete=models.CASCADE,related_name="followed")
    value = models.CharField(max_length=100,blank=False,choices=(("Following","Following"),("Follow","Follow")))