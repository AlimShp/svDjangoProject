from django.db import models

# Create your models here.
class ModelReg(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    user_session = models.CharField(max_length=48)
    user_image = models.CharField(null=True, max_length=260)

class ProfileImg(models.Model):
    ваше_фото = models.ImageField(upload_to='app/static/img')



