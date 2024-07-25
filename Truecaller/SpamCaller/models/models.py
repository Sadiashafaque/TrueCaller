from django.db import models
from django.contrib.auth.models import User

class RegisteredProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    phone = models.IntegerField(null=False, unique=True)
    spam = models.BooleanField(default=False)
    email=models.EmailField(max_length=50, null=True)

    def __str__(self):
        return str(self.user)
    
class Contact(models.Model):
    name = models.CharField(max_length=100, null=False)
    phone = models.IntegerField(null=False)
    spam = models.BooleanField(default=False)
    email=models.EmailField(max_length=50, null=True)

    def __str__(self):
        return self.name
    
    
class RandomSpam(models.Model):
     phone_number = models.IntegerField(null=False, unique=True)

     def __str__(self):
          return str(self.phone_number)


class ContactsProfilesMapping(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.profile} ({self.contact})"