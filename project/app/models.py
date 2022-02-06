from django.db import models

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=50, null=False)
    def __str__(self):
        return str(self.name)


class Quiz(models.Model):
    name=models.CharField(max_length=20, null=False)
    user_app=models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.name)