from django.db import models
from django.contrib.auth.models import User

# Create your models here.

    
class Genre(models.Model):
    genre_name = models.CharField(max_length=50)
    
class Profile(models.Model):
    user_info = models.OneToOneField(User,on_delete=models.CASCADE)
    user_nick = models.CharField(max_length=20)



class Sign_up(models.Model):
    user_id = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    password_again = models.CharField(max_length=20,default=None)

class Organize(models.Model):
    year_date = models.IntegerField()
    month_date = models.IntegerField(null=True)
    day_date = models.IntegerField(null=True)
    organize_id = models.ForeignKey(Genre,on_delete=models.CASCADE,default = '', db_column='organize_id')
    contents = models.TextField()
    u_id = models.IntegerField(default=None)
    # u_id = models.ForeignKey(Sign_up,on_delete=models.CASCADE,default = '', db_column='u_id')
    img_file = models.ImageField(default=None,null=True,blank=True,upload_to="")
    hide_data = models.CharField(max_length=10,default=None,null=True)
    like = models.ManyToManyField(Sign_up,related_name='like_user',blank=True)
    like_count = models.IntegerField(default=0)
    like_drf = models.ManyToManyField(Profile,related_name='like_nick',blank=True)
    like_count_drf = models.IntegerField(default=0)
    # blank=True 는 필드가 폼(입력 양식)에서 빈 채로 저장되는 것을 허용.
     

class Follow(models.Model):
    follower = models.CharField(max_length=20)
    following = models.TextField(null=True,default=None)        
    
class DRF_Follow(models.Model):
    user = models.CharField(max_length=20)
    friend = models.CharField(max_length=20)
    