from django.db import models

class Transporter(models.Model):
    TransporterName = models.CharField(max_length=100,null=True,blank=True)
    TransporterAddress = models.CharField(max_length=100,null=True,blank=True)
    Transporter_Contact = models.CharField(max_length=30)
    Transporter_Email = models.EmailField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.TransporterName  if self.TransporterName else "Unnamed Transporter"

class Driver(models.Model):
    Driver_Name = models.CharField(max_length=100,null=False,blank=False)
    Driver_Contact = models.CharField(max_length=20)
    Driver_Email = models.EmailField(max_length=100,null=True,blank=True)
    Vehicle_Number = models.CharField(max_length=100, null=True, blank=True)
    Driver_Location = models.CharField(max_length=100,null=True,blank=True)

    # Relationship
    Transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.Driver_Name
    

