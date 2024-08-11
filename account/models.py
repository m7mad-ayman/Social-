from django.db import models
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
import uuid

# Create your models here.
class Confirm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username =models.CharField(max_length=100,blank=False)
    password = models.CharField(max_length=100,blank=False,validators=[validate_password])
    email = models.CharField(max_length=100,unique=True)
    code = models.CharField(max_length=100,blank=False)
    expire = models.DateTimeField(null=False,blank=False)

class Profile(models.Model):
    User = get_user_model()
    user = models.ForeignKey(User,blank=False,on_delete=models.CASCADE)
    bio = models.CharField(max_length=400,blank=False,null=False,default="Your bio on social media")
    img = models.ImageField(upload_to='media/img/%y/',blank=False,default="media/img/24/profile.png")
    followers = models.IntegerField(default=0,blank=False,null=False)
    following = models.IntegerField(default=0,blank=False,null=False)
    posts = models.IntegerField(default=0,blank=False,null=False)
    def __str__(self):
        return self.user.username
