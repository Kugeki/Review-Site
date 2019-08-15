from django.db import models

class Person(models.Model):
    account = models.CharField(max_length=200, blank=True, null=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.first_name

class Review(models.Model):
    # session_key = models.CharField(max_length=128, null=True, blank=True, default=None)
    blogger = models.OneToOneField(Person, null=True, on_delete=models.SET_NULL, related_name='blogger')
    person = models.OneToOneField(Person, null=True, on_delete=models.SET_NULL, related_name='person')
 
    content = models.TextField()
    rating = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.blogger.first_name + " - " + str(self.rating)