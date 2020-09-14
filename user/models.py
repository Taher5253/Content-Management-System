from django.db import models
from django.core.validators import RegexValidator
import os
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Cms_user(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^[789]\d{9}$', message="Phone number is not valid")
    phone_number = models.CharField(validators=[phone_regex], max_length=10)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    pincode = models.CharField(max_length=6, validators=[RegexValidator(r'^[0-9]\d*$')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name


class Categories(models.Model):
    category_type = models.CharField(max_length=20)

class Content(models.Model):
    content_author = models.ForeignKey(Cms_user, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    body = models.CharField(max_length=300)
    summary = models.CharField(max_length=60)
    document_pdf = models.FileField()



    def delete(self, *args, **kwargs):
        if os.path.isfile(self.document_pdf.path):
            os.remove(self.document_pdf.path)

        super(Content, self).delete(*args,**kwargs)

class content_category(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)


