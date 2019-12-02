from django.db import models

class Department(models.Model):
    name = models.TextField(blank=True,null=True)
    def __str__(self):
        return self.name


class Profile(models.Model):
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    enrollment = models.IntegerField(blank=True,null=True,unique=True)
    name = models.TextField(blank=True,null=True)
    semester = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return str(self.enrollment)
        

