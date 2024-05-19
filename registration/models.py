from django.db import models

# Create your models here.
class UserProfile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    resume = models.FileField(upload_to='resumes/')

    class Meta:
        app_label = 'registration'
    
