from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
# from helpdesk.customadmin.models import Company

    
class Country(models.Model):
    name= models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

class CustomUser(AbstractUser):
    signup_as_choices = (
        ('T', 'tenat'),
        ('L', 'Landload')
    )
    status_choice=(
        ('watting','Watting'),
        ('approved','Approved'),
        ('rejected','Rejected')
    )
    username = None
    email = models.EmailField(_('email address'), unique=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    status = models.CharField(choices=status_choice,max_length=100,default='watting')
    delete_status = models.BooleanField(default=1)
    token = models.CharField(max_length=16)
    phone_number=models.CharField(max_length=10,null=True,blank=True)
    image = models.ImageField(upload_to='user_profile/', null=True,blank=True)
    address = models.CharField(max_length=500,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    zipcode = models.CharField(max_length=8,null=True,blank=True)
    country =models.ForeignKey(Country,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.email

    def delete(self, using=None, keep_parents=False):
        self.image.storage.delete(self.image.name)
        super().delete()


class ForgetPassMailVerify(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    link=models.CharField(max_length=500)
    verify = models.BooleanField(default=False)

    def __str__(self):
        return self.user

class UserEmailVerify(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    link = models.CharField(max_length=500)
    verify = models.BooleanField(default=False)

    def __str__(self):
        return self.user
    
class UserNumberVerify(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    verify = models.BooleanField(default=False)

    def __str__(self):
        return self.user

class DocumentSetModel(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    has_backside = models.BooleanField(default=False)
    ocr_Labels =models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name

class CustomerModel(models.Model):
    surname_choice=(
        ('mr.','MR.'),
        ('mrs.','Mrs'),
    )
    gender_choices = (
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Intersex', 'Intersex'),
        ('MtF Female', 'MtF Female'),
        ('FtM Male', 'FtM Male'),
    )
    surname = models.CharField(max_length=255,choices=surname_choice,default='mr.')
    firstname = models.CharField(max_length=255,blank=True,null=True)
    nationality = models.ForeignKey(Country,on_delete=models.CASCADE,null=True,blank=True)
    gender = models.CharField(max_length=255,choices=gender_choices,blank=True,null=True)
    createdBy = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)

class CustomerDocumentModel(models.Model):
    customer =models.ForeignKey(CustomerModel,on_delete=models.CASCADE,null=True,blank=True)
    attached_file = models.FileField(upload_to='document/%Y/%M/')
    extracted_json = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
