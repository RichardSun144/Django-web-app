from django.db import models

# Create your models here.

class UserInfo(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    isDriver = models.BooleanField(default=False)
    #pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.username + "  " + self.email
   
class DriverInfo(models.Model):
  owner = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
  vehicleType = models.CharField(max_length=32)
  licenseNumber = models.CharField(max_length=32)
  containNumber = models.IntegerField()
  specialText = models.TextField(blank=True, default= "")
  def __str__(self):
        return self.vehicleType 
 
  
'''
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
        '''