from django.db import models


class ClientVst(models.Model):

    Client_Name = models.CharField,
    Client_Phone =models.IntegerField,
    Client_Company = models.CharField,
    Purpose_visit =models.CharField,
    Date_visit=models.DateField,
    Meeting_Summary = models.DateFieldcd..